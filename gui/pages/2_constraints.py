import os
import sys

import streamlit as st
import json
from pathlib import Path

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if repo_root not in sys.path:
    sys.path.append(repo_root)

from core.solver import main  # now it works

st.title("🛠️ Roster Constraints")
CONFIG_PATH = Path("/Users/astra/My Code/callibrium/config.json")

# Check if setup exists
if not all(k in st.session_state for k in ["shifts", "assignees", "start_date", "end_date"]):
    st.warning("Please complete the Setup page first.")
else:
    shifts = st.session_state.shifts
    assignees = st.session_state.assignees

    # Coverage defaults
    st.subheader("Coverage Defaults")
    coverage_default_min = st.number_input("Default min per shift", value=2, min_value=0)
    coverage_default_max = st.number_input("Default max per shift", value=2, min_value=1)

    # Dynamic shift coverage
    weekend_coverage = {}
    weekday_coverage = {}
    st.subheader("Weekend Coverage")
    for shift in shifts:
        col1, col2 = st.columns(2)
        with col1:
            weekend_min = st.number_input(f"{shift} weekend min", value=1, min_value=0, key=f"{shift}_weekend_min")
        with col2:
            weekend_max = st.number_input(f"{shift} weekend max", value=2, min_value=1, key=f"{shift}_weekend_max")
        weekend_coverage[shift] = {"min": weekend_min, "max": weekend_max}

    st.subheader("Weekday Coverage")
    for shift in shifts:
        col1, col2 = st.columns(2)
        with col1:
            weekday_min = st.number_input(f"{shift} weekday min", value=1, min_value=0, key=f"{shift}_weekday_min")
        with col2:
            weekday_max = st.number_input(f"{shift} weekday max", value=2, min_value=1, key=f"{shift}_weekday_max")
        weekday_coverage[shift] = {"min": weekday_min, "max": weekday_max}

    # Fairness
    st.subheader("Fairness")
    min_shifts = st.number_input("Minimum shifts per assignee", value=1, min_value=0)
    balance = st.selectbox("Balance type", ["tight", "medium", "loose"], index=2)

    # Weekend fairness
    st.subheader("Weekend Fairness")
    weekend_strict = st.checkbox("Strict weekend fairness?", value=False)
    weekend_weight = st.number_input("Weekend fairness weight", value=1, min_value=0)

    # Consecutive shifts
    st.subheader("Consecutive Shifts")
    min_gap = st.number_input("Minimum gap between consecutive shifts", value=0, min_value=0)

    # Generate and save JSON
    if st.button("Generate and Save Configuration"):
        config = {
            "start_date": st.session_state.start_date,
            "end_date": st.session_state.end_date,
            "shifts": shifts,
            "assignees": assignees,
            "constraints": {
                "coverage": {
                    "default": {"min": coverage_default_min, "max": coverage_default_max},
                    "weekend": weekend_coverage,
                    "weekday": weekday_coverage
                },
                "fairness": {"min_shifts": min_shifts, "balance": balance},
                "weekend_fairness": {"strict": weekend_strict, "weight": weekend_weight},
                "no_consecutive": {"min_gap": min_gap}
            }
        }

        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)

        st.success(f"✅ Configuration saved to {CONFIG_PATH}")
        # st.json(config)

        if st.button("Run Solver"):
            with st.spinner("Solver is running..."):
                result = main()
            st.success("Solver finished! Go to Results")
            st.write("Result:", result)
