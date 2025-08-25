from datetime import datetime, timedelta

def generate_timeblocks(start_date, end_date, shifts):
    """Generate time blocks using actual dates and detect weekends."""
    blocks = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end - start).days + 1

    for d in range(total_days):
        current_date = start + timedelta(days=d)
        is_weekend = current_date.weekday() in [5, 6]  # Saturday=5, Sunday=6
        for s in shifts:
            blocks.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_index": d + 1,
                "shift": s,
                "is_weekend": is_weekend
            })
    return blocks
