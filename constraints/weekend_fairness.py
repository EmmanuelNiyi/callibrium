class WeekendFairnessConstraint:
    @staticmethod
    def apply(model, vars, assignees, blocks, params=None):
        """
        Ensures weekend shifts are fairly distributed among assignees.

        Arguments:
        ----------
        model: cp_model.CpModel
            The OR-Tools model instance.
        vars: dict
            Dictionary of assignment variables {(assignee, date, shift): BoolVar}.
        assignees: list
            List of all assignees.
        blocks: list
            List of time block dictionaries generated from `generate_timeblocks`.
        params: dict
            Optional parameters, like {
                "strict": True/False (strict equality or soft balancing)
            }
        """
        if params is None:
            params = {}

        strict = params.get("strict", True)

        # Identify weekend blocks
        weekend_blocks = [b for b in blocks if b["is_weekend"]]
        if not weekend_blocks:
            return  # no weekends to balance

        total_weekends = len(weekend_blocks)
        base_weekends = total_weekends // len(assignees)
        remainder = total_weekends % len(assignees)

        for i, name in enumerate(assignees):
            # Count how many weekend shifts this assignee has
            weekend_count = sum(vars[(name, b["date"], b["shift"])]
                                for b in weekend_blocks)

            if strict:
                # Strictly equal distribution (some may get +1 due to remainder)
                if i < remainder:
                    model.Add(weekend_count == base_weekends + 1)
                else:
                    model.Add(weekend_count == base_weekends)
            else:
                # Soft fairness: allow a range for balancing flexibility
                model.Add(weekend_count >= base_weekends)
                model.Add(weekend_count <= base_weekends + 1)
