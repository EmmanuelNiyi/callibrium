import json
import importlib
from ortools.sat.python import cp_model


# -----------------------------
# Constraint Base Class
# -----------------------------
class BaseConstraint:
    name: str

    def apply(self, model: cp_model.CpModel, variables, params: dict):
        raise NotImplementedError


# -----------------------------
# Constraint 1: Coverage
# -----------------------------
class CoverageConstraint(BaseConstraint):
    name = "coverage"

    def apply(self, model, variables, params):
        """Ensure exactly `num_needed` people are assigned per day"""
        days = variables["days"]
        assignees = variables["assignees"]

        num_needed = params.get("num_needed", 1)  # default to 1 if not specified

        for d in days:
            model.Add(sum(assignees[name][d] for name in assignees) == num_needed)


# -----------------------------
# Constraint 2: Fairness
# -----------------------------
class FairnessConstraint(BaseConstraint):
    name = "fairness"

    def apply(self, model, variables, params):
        """Ensure shifts are fairly distributed"""
        assignees = variables["assignees"]
        days = variables["days"]

        totals = {name: sum(vars) for name, vars in assignees.items()}

        min_total = model.NewIntVar(0, len(days), "min_total")
        max_total = model.NewIntVar(0, len(days), "max_total")

        model.AddMinEquality(min_total, list(totals.values()))
        model.AddMaxEquality(max_total, list(totals.values()))

        max_diff = params.get("max_difference", 1)
        model.Add(max_total - min_total <= max_diff)


# -----------------------------
# Constraint Loader
# -----------------------------
def load_constraints():
    return {
        "coverage": CoverageConstraint,
        "fairness": FairnessConstraint,
    }


# -----------------------------
# Solver Builder
# -----------------------------
def build_solver(config_path="config.json"):
    with open(config_path) as f:
        config = json.load(f)

    model = cp_model.CpModel()

    # --- Step 1: Variables ---
    days = range(config["days"])
    assignees = config["assignees"]

    assignments = {
        name: [model.NewBoolVar(f"{name}_day{d}") for d in days]
        for name in assignees
    }

    variables = {"days": days, "assignees": assignments}

    # --- Step 2: Apply constraints ---
    available_constraints = load_constraints()
    for c_cfg in config["constraints"]:
        cname = c_cfg["name"]
        params = c_cfg.get("params", {})

        if cname not in available_constraints:
            raise ValueError(f"Unknown constraint: {cname}")

        constraint = available_constraints[cname]()
        constraint.apply(model, variables, params)

    return model, variables


# -----------------------------
# Run Example
# -----------------------------
if __name__ == "__main__":
    model, variables = build_solver("config.json")

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        days = variables["days"]
        assignees = variables["assignees"]

        print("📅 Schedule:")
        for d in days:
            assigned = [name for name, vars in assignees.items() if solver.Value(vars[d]) == 1]
            print(f"  Day {d+1}: {', '.join(assigned)}")

        print("\n📊 Shifts per person:")
        for name, vars in assignees.items():
            total = sum(solver.Value(v) for v in vars)
            print(f"  {name}: {total}")
    else:
        print("❌ No solution found")

