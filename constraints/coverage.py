# constraints/coverage.py
from ortools.sat.python import cp_model


class CoverageConstraint:
    @staticmethod
    def apply(model, vars, assignees, blocks, params=None):
        """
        Enforce dynamic coverage rules:
        - Weekend vs weekday
        - Shift-specific overrides
        """
        if params is None:
            params = {}

        A, B = len(assignees), len(blocks)

        default_rule = params.get("default", {"min": 1, "max": 1})
        weekend_rules = params.get("weekend", {})
        weekday_rules = params.get("weekday", {})

        for b, block in enumerate(blocks):
            shift = block["shift"]
            is_weekend = block["is_weekend"]

            # Select rules based on day type and shift label
            if is_weekend:
                rule = weekend_rules.get(shift, weekend_rules.get("default", default_rule))
            else:
                rule = weekday_rules.get(shift, weekday_rules.get("default", default_rule))

            min_cover = rule.get("min", default_rule["min"])
            max_cover = rule.get("max", default_rule["max"])

            assigned = [vars[a][b] for a in range(A)]
            model.Add(sum(assigned) >= min_cover)
            model.Add(sum(assigned) <= max_cover)