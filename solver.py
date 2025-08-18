import json
from ortools.sat.python import cp_model
from utils.loader import load_constraints


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
