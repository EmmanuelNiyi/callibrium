from ortools.sat.python import cp_model


def build_model(config, constraints, blocks):
    model = cp_model.CpModel()
    A, B = len(config["assignees"]), len(blocks)

    vars = [
        [model.NewBoolVar(f"x_{a}_{b}") for b in range(B)]
        for a in range(A)
    ]

    # Apply constraints with parameters
    for cname, params in config["constraints"].items():
        constraints[cname].apply(model, vars, config["assignees"], blocks, params)

    return model, vars
