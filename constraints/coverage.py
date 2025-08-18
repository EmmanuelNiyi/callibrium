from .base import BaseConstraint


class CoverageConstraint(BaseConstraint):
    name = "coverage"

    def apply(self, model, variables, params):
        days = variables["days"]
        assignees = variables["assignees"]
        num_needed = params.get("num_needed", 1)

        for d in days:
            model.Add(sum(assignees[name][d] for name in assignees) == num_needed)
