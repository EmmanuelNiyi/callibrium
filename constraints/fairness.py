from .base import BaseConstraint


class FairnessConstraint(BaseConstraint):
    name = "fairness"

    def apply(self, model, variables, params):
        assignees = variables["assignees"]
        days = variables["days"]

        totals = {name: sum(vars) for name, vars in assignees.items()}

        min_total = model.NewIntVar(0, len(days), "min_total")
        max_total = model.NewIntVar(0, len(days), "max_total")

        model.AddMinEquality(min_total, list(totals.values()))
        model.AddMaxEquality(max_total, list(totals.values()))

        max_diff = params.get("max_difference", 1)
        model.Add(max_total - min_total <= max_diff)
