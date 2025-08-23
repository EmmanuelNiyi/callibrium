import json
from ortools.sat.python import cp_model

from utils.output import print_schedule, print_totals, export_roster_to_csv, convert_roster_to_html
from utils.timeblocks import generate_timeblocks
import constraints.coverage as coverage
import constraints.fairness as fairness
import constraints.no_consecutive as no_consecutive
import model as mdl


def main():
    # Load config
    with open("config.json") as f:
        config = json.load(f)

    # Generate blocks
    blocks = generate_timeblocks(config["start_date"], config["end_date"], config["shifts"])

    # Map constraints
    constraint_map = {
        "coverage": coverage.CoverageConstraint,
        "no_consecutive": no_consecutive,
        "weekend_fairness": fairness.WeekendFairnessConstraint,
        "fairness": fairness.BaseFairnessConstraint,
    }

    # Build model
    model, vars = mdl.build_model(config, constraint_map, blocks)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        # Organize schedule by day and shift
        schedule = {}
        for b, block in enumerate(blocks):
            date = block["date"]
            shift = block["shift"]
            assigned = [config["assignees"][a] for a in range(len(config["assignees"]))
                        if solver.Value(vars[a][b]) == 1]
            if date not in schedule:
                schedule[date] = {}
            schedule[date][shift] = assigned

        print_schedule(schedule, config)
        print_totals(vars, solver, blocks, config)

        export_roster_to_csv(schedule)
        convert_roster_to_html(schedule)

    else:
        print("❌ No solution found")


if __name__ == "__main__":
    main()
