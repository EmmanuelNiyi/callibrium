from ortools.sat.python import cp_model


# --- Constraint Plugins ---
def add_num_assignees_constraint(model, x, config):
    assignees = config["assignees"]
    days = config["days"]
    num_needed = config["num_needed"]
    for d in range(days):
        model.Add(sum(x[a, d] for a in assignees) == num_needed)


def add_rest_constraint(model, x, config):
    assignees = config["assignees"]
    days = config["days"]
    rest_days = config["rest_days"]
    for a in assignees:
        for d in range(days - rest_days):
            model.Add(x[a, d] + x[a, d + 1] <= 1)


def add_unavailability_constraint(model, x, config):
    unavailable = config["unavailable"]
    for (a, d) in unavailable:
        model.Add(x[a, d] == 0)


def add_soft_fair_distribution(model, x, config, fairness_vars):
    assignees = config["assignees"]
    days = config["days"]

    # Shifts per assignee
    shifts_per_a = {a: sum(x[a, d] for d in range(days)) for a in assignees}

    # Variables for max and min
    max_shifts = model.NewIntVar(0, days, "max_shifts")
    min_shifts = model.NewIntVar(0, days, "min_shifts")

    for a in assignees:
        model.Add(shifts_per_a[a] <= max_shifts)
        model.Add(shifts_per_a[a] >= min_shifts)

    # Keep references so we can build objective later
    fairness_vars["max_shifts"] = max_shifts
    fairness_vars["min_shifts"] = min_shifts


# --- Constraint Registry ---
constraint_registry = {
    "num_assignees": add_num_assignees_constraint,
    "rest": add_rest_constraint,
    "unavailability": add_unavailability_constraint,
    "fair_distribution": add_soft_fair_distribution,  # soft fairness
}


# --- Solver Wrapper ---
def solve_schedule(config):
    model = cp_model.CpModel()

    # Decision variables
    x = {(a, d): model.NewBoolVar(f"{a}_day{d}")
         for a in config["assignees"] for d in range(config["days"])}

    # Store extra vars for fairness objective
    fairness_vars = {}

    # Apply active constraints
    for key, constraint_fn in constraint_registry.items():
        if config.get(f"use_{key}", False):
            if key == "fair_distribution":
                constraint_fn(model, x, config, fairness_vars)
            else:
                constraint_fn(model, x, config)

    # Add soft fairness objective
    if "max_shifts" in fairness_vars and "min_shifts" in fairness_vars:
        imbalance = model.NewIntVar(0, config["days"], "imbalance")
        model.Add(imbalance == fairness_vars["max_shifts"] - fairness_vars["min_shifts"])
        model.Minimize(imbalance)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5  # optional timeout
    status = solver.Solve(model)

    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        schedule = {}
        shift_counts = {a: 0 for a in config["assignees"]}
        for d in range(config["days"]):
            workers = [a for a in config["assignees"] if solver.Value(x[a, d]) == 1]
            schedule[d + 1] = workers
            for a in workers:
                shift_counts[a] += 1
        return schedule, shift_counts
    else:
        return None, None


# --- Example Run ---
if __name__ == "__main__":
    config = {
        "days": 7,
        "assignees": ["Alice", "Bob", "Charlie", "David"],
        "num_needed": 2,
        "rest_days": 1,
        "unavailable": {("Alice", 3)},

        # toggles
        "use_num_assignees": True,
        "use_rest": True,
        "use_unavailability": True,
        "use_fair_distribution": True,
    }

    schedule, shift_counts = solve_schedule(config)

    if schedule:
        print("📅 Schedule:")
        for day, workers in schedule.items():
            print(f"  Day {day}: {', '.join(workers)}")

        print("\n📊 Shifts per person:")
        for a, count in shift_counts.items():
            print(f"  {a}: {count}")
    else:
        print("No solution found.")
