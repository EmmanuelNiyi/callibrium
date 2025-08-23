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
        if params is None:
            params = {}

        num_assignees = len(assignees)
        weekend_indices = [i for i, blk in enumerate(blocks) if blk.get("is_weekend", False)]

        if not weekend_indices:
            return None  # no weekend fairness needed

        total_weekend_blocks = len(weekend_indices)
        weekend_shifts_per_assignee = [
            sum(vars[a][b] for b in weekend_indices)
            for a in range(num_assignees)
        ]

        min_weekend = model.NewIntVar(0, total_weekend_blocks, "min_weekend")
        max_weekend = model.NewIntVar(0, total_weekend_blocks, "max_weekend")
        model.AddMinEquality(min_weekend, weekend_shifts_per_assignee)
        model.AddMaxEquality(max_weekend, weekend_shifts_per_assignee)

        diff_weekend = model.NewIntVar(0, total_weekend_blocks, "diff_weekend")
        model.Add(diff_weekend == max_weekend - min_weekend)

        return diff_weekend

