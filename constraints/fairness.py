# constraints/fairness.py
from ortools.sat.python import cp_model
import math


class FairnessConstraint:
    @staticmethod
    def apply(model, vars, assignees, blocks, params=None):
        """
        Fully configurable soft fairness with min assignment:
        - min_shifts: minimum shifts per assignee
        - balance: "tight", "medium", "loose", "soft"
        - Softly minimizes the difference between max and min assigned shifts
        """
        if params is None:
            params = {}

        total_blocks = len(blocks)
        num_assignees = len(assignees)
        min_shifts_per_person = params.get("min_shifts", 1)
        balance = params.get("balance", "soft")

        # Compute tolerance based on balance
        if balance == "tight":
            tolerance = 0
        elif balance == "medium":
            tolerance = 1
        elif balance == "loose":
            tolerance = 2
        else:  # soft
            tolerance = math.ceil(total_blocks / num_assignees / 2)

        # Compute total shifts per assignee
        shifts_per_assignee = [sum(vars[a][b] for b in range(total_blocks)) for a in range(num_assignees)]

        # Enforce minimum assignment per person
        for a in range(num_assignees):
            model.Add(shifts_per_assignee[a] >= min_shifts_per_person)

        # Softly enforce upper bound based on tolerance
        avg = total_blocks / num_assignees
        for a in range(num_assignees):
            model.Add(shifts_per_assignee[a] <= math.ceil(avg + tolerance))

        # Min and max shifts variables
        min_shifts = model.NewIntVar(0, total_blocks, "min_shifts")
        max_shifts = model.NewIntVar(0, total_blocks, "max_shifts")
        model.AddMinEquality(min_shifts, shifts_per_assignee)
        model.AddMaxEquality(max_shifts, shifts_per_assignee)

        # Soft fairness: minimize difference between max and min
        diff = model.NewIntVar(0, total_blocks, "diff_max_min")
        model.Add(diff == max_shifts - min_shifts)
        model.Minimize(diff)
