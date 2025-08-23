# constraints/fairness.py
from ortools.sat.python import cp_model
import math


class BaseFairnessConstraint:
    @staticmethod
    def apply(model, vars, assignees, blocks, params=None):
        if params is None:
            params = {}

        total_blocks = len(blocks)
        num_assignees = len(assignees)
        min_shifts = params.get("min_shifts", 1)
        balance = params.get("balance", "soft")

        shifts_per_assignee = [
            sum(vars[a][b] for b in range(total_blocks))
            for a in range(num_assignees)
        ]

        # Lower bounds
        for a in range(num_assignees):
            model.Add(shifts_per_assignee[a] >= min_shifts)

        # Balance tolerance
        avg = total_blocks / num_assignees
        tolerance = {"tight": 0, "medium": 1, "loose": 2}.get(
            balance, math.ceil(avg / 2)
        )

        for a in range(num_assignees):
            model.Add(shifts_per_assignee[a] <= math.ceil(avg + tolerance))

        # Min and max shifts for fairness metric
        min_shifts_var = model.NewIntVar(0, total_blocks, "min_shifts")
        max_shifts_var = model.NewIntVar(0, total_blocks, "max_shifts")
        model.AddMinEquality(min_shifts_var, shifts_per_assignee)
        model.AddMaxEquality(max_shifts_var, shifts_per_assignee)

        diff_var = model.NewIntVar(0, total_blocks, "diff_total")
        model.Add(diff_var == max_shifts_var - min_shifts_var)

        return diff_var


class WeekendFairnessConstraint:
    @staticmethod
    def apply(model, vars, assignees, blocks, params=None):
        """
        Distributes weekend shifts inversely proportional to total calls:
        - Fewer total shifts → more weekends
        - More total shifts → fewer weekends

        Returns an IntVar representing the deviation for the objective.
        """
        if params is None:
            params = {}

        strict = params.get("strict", False)

        # Identify weekend blocks
        weekend_indices = [i for i, b in enumerate(blocks) if b["is_weekend"]]
        if not weekend_indices:
            return model.NewIntVar(0, 0, "no_weekend_diff")

        total_weekends = len(weekend_indices)
        num_assignees = len(assignees)

        # --- Count total shifts for each assignee ---
        total_shifts = []
        for a_idx in range(num_assignees):
            total = model.NewIntVar(0, len(blocks), f"total_shifts_{a_idx}")
            model.Add(total == sum(vars[a_idx][b] for b in range(len(blocks))))
            total_shifts.append(total)

        # --- Count weekend shifts for each assignee ---
        weekend_counts = []
        for a_idx in range(num_assignees):
            wc = model.NewIntVar(0, total_weekends, f"weekend_count_{a_idx}")
            model.Add(wc == sum(vars[a_idx][b] for b in weekend_indices))
            weekend_counts.append(wc)

        # --- Compute max total shifts (for inverse weighting) ---
        max_shifts = model.NewIntVar(0, len(blocks), "max_shifts")
        model.AddMaxEquality(max_shifts, total_shifts)

        # --- Create fairness deviation variable ---
        max_deviation = model.NewIntVar(0, total_weekends, "max_weekend_dev")

        for a_idx in range(num_assignees):
            # "Slack" = how far this assignee is from max load (more slack → should have more weekends)
            slack = model.NewIntVar(0, len(blocks), f"slack_{a_idx}")
            model.Add(slack == max_shifts - total_shifts[a_idx])

            # Ideal weekend count ~ slack ratio scaled to total weekends
            # Approximation: round proportional share without complex division
            ideal_weekends = model.NewIntVar(0, total_weekends, f"ideal_weekends_{a_idx}")
            model.Add(ideal_weekends * num_assignees <= slack * total_weekends + total_weekends // 2)

            # Deviation = |actual weekends - ideal weekends|
            over = model.NewIntVar(0, total_weekends, f"over_{a_idx}")
            under = model.NewIntVar(0, total_weekends, f"under_{a_idx}")

            model.Add(over >= weekend_counts[a_idx] - ideal_weekends)
            model.Add(under >= ideal_weekends - weekend_counts[a_idx])

            deviation = model.NewIntVar(0, total_weekends, f"deviation_{a_idx}")
            model.Add(deviation == over + under)
            model.Add(deviation <= max_deviation)

        return max_deviation




