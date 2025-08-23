def apply(model, vars, assignees, blocks, params=None):
    min_gap = 1
    if params:
        min_gap = params.get("min_gap", 2)

    for a in range(len(assignees)):
        for i in range(len(blocks)):
            for j in range(i+1, min(i+1+min_gap, len(blocks))):
                model.Add(vars[a][i] + vars[a][j] <= 1)
