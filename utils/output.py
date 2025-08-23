import csv
from datetime import datetime


def print_schedule(schedule, config):
    """Print the full schedule in a readable format."""
    print("📅 Schedule:")
    for date in sorted(schedule.keys()):
        print(f"{date}:")
        for shift in config["shifts"]:
            names = ", ".join(schedule[date].get(shift, []))
            print(f"  {shift}: {names}")


def print_totals(vars, solver, blocks, config):
    """Print total shifts and weekend shifts per assignee."""
    totals = {name: 0 for name in config["assignees"]}
    weekend_totals = {name: 0 for name in config["assignees"]}

    for a, name in enumerate(config["assignees"]):
        for b, block in enumerate(blocks):
            if solver.Value(vars[a][b]) == 1:
                totals[name] += 1
                if block["is_weekend"]:
                    weekend_totals[name] += 1

    print("\n📊 Shifts per person (Total and Weekend):")
    for name in config["assignees"]:
        print(f"{name}: Total = {totals[name]}, Weekend = {weekend_totals[name]}")


def export_roster_to_csv(schedule, filename="roster.csv"):
    """
    Converts a schedule dictionary into a CSV roster file,
    including day of the week and totals at the bottom.
    """
    # Get all unique shift types (columns)
    shifts = sorted({shift for day in schedule.values() for shift in day})

    # Initialize counters for totals and weekend totals
    totals = {}
    weekend_totals = {}

    for day, assignments in schedule.items():
        day_name = datetime.strptime(day, "%Y-%m-%d").strftime("%A")
        is_weekend = day_name in ["Saturday", "Sunday"]

        for shift, names in assignments.items():
            for name in names:
                totals[name] = totals.get(name, 0) + 1
                if is_weekend:
                    weekend_totals[name] = weekend_totals.get(name, 0) + 1

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow(["Date", "Day"] + shifts)

        # Write schedule rows
        for date, assignments in sorted(schedule.items()):
            day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
            row = [date, day_name] + [", ".join(assignments.get(shift, [])) for shift in shifts]
            writer.writerow(row)

        # Add empty line before totals
        writer.writerow([])
        writer.writerow([])
        writer.writerow([])
        writer.writerow(["Summary 📊"])
        writer.writerow(["Name", "Total Shifts", "Weekend Shifts"])

        # Write totals for each assignee
        for name in sorted(totals):
            writer.writerow([name, totals[name], weekend_totals.get(name, 0)])

    print(f"✅ Roster with totals successfully exported to {filename}")


def convert_roster_to_html(schedule):
    """
    Converts the schedule dictionary into a styled HTML table string,
    including totals at the bottom.
    """
    # Extract unique shift names
    shifts = sorted({shift for day in schedule.values() for shift in day})

    # --- Calculate totals and weekend totals ---
    totals = {}
    weekend_totals = {}
    for day, assignments in schedule.items():
        day_name = datetime.strptime(day, "%Y-%m-%d").strftime("%A")
        is_weekend = day_name in ["Saturday", "Sunday"]
        for shift, names in assignments.items():
            for name in names:
                totals[name] = totals.get(name, 0) + 1
                if is_weekend:
                    weekend_totals[name] = weekend_totals.get(name, 0) + 1

    # --- Style for the HTML table ---
    style = """
    <style>
        table { border-collapse: collapse; width: 80%; margin: 20px auto; font-family: Arial, sans-serif; }
        th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: center; }
        th { background-color: #f2f2f2; font-weight: bold; }
        h2 { text-align: center; }
    </style>
    """

    # --- Schedule Table ---
    html = style + "<h2>Duty Roster</h2>"
    html += "<table><tr><th>Date</th><th>Day</th>" + "".join(f"<th>{shift}</th>" for shift in shifts) + "</tr>"

    for date, assignments in sorted(schedule.items()):
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        html += "<tr>"
        html += f"<td>{date}</td><td>{day_name}</td>"
        html += "".join(f"<td>{', '.join(assignments.get(shift, []))}</td>" for shift in shifts)
        html += "</tr>"

    html += "</table>"

    # --- Totals Table ---
    html += "<h2>Totals</h2>"
    html += "<table><tr><th>Name</th><th>Total Shifts</th><th>Weekend Shifts</th></tr>"

    for name in sorted(totals):
        html += f"<tr><td>{name}</td><td>{totals[name]}</td><td>{weekend_totals.get(name, 0)}</td></tr>"

    html += "</table>"

    # Save to an HTML file
    with open("roster.html", "w") as f:
        f.write(html)

    print("✅ HTML roster saved to roster.html")

    return html
