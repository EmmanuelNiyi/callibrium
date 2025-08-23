from ortools.sat.python import cp_model


def build_model(config, constraints, blocks):
    model = cp_model.CpModel()
    A, B = len(config["assignees"]), len(blocks)

    # Binary variables for assignments
    vars = [
        [model.NewBoolVar(f"x_{a}_{b}") for b in range(B)]
        for a in range(A)
    ]

    # Collect fairness difference variables (to combine later)
    fairness_vars = {}

    # Apply constraints
    for cname, params in config["constraints"].items():
        if cname in ["fairness", "weekend_fairness"]:
            # Capture fairness variables for unified objective
            fairness_vars[cname] = constraints[cname].apply(
                model, vars, config["assignees"], blocks, params
            )
        else:
            # Apply all other constraints directly
            constraints[cname].apply(
                model, vars, config["assignees"], blocks, params
            )

    # --------------------------
    # Unified Objective
    # --------------------------
    diff_total = fairness_vars.get("fairness")
    diff_weekend = fairness_vars.get("weekend_fairness")
    weight_weekend = config["constraints"]["weekend_fairness"].get("weight", 0)

    if diff_total is None:
        raise ValueError("Base fairness constraint must return a diff variable.")

    if diff_weekend is not None:
        # Combine base fairness + weighted weekend fairness
        total_objective = model.NewIntVar(0, 1000, "total_objective")
        model.Add(total_objective == diff_total + (weight_weekend * diff_weekend))
        model.Minimize(total_objective)
    else:
        # Minimize only base fairness if no weekend fairness returned
        model.Minimize(diff_total)

    return model, vars
