import streamlit as st
from datetime import date

st.title("🗓️ Roster Setup")

# Initialize session state
if "setup_done" not in st.session_state:
    st.session_state.setup_done = False

# Schedule Period
start_date = st.date_input("Start Date", value=date(2025, 8, 1))
end_date = st.date_input("End Date", value=date(2025, 8, 31))

# Shifts — dynamic
shifts_input = st.text_area(
    "Enter shift types (comma-separated)",
    value="MEU, WARD"
)
shifts = [s.strip() for s in shifts_input.split(",") if s.strip()]

# Assignees — dynamic
assignees_input = st.text_area(
    "Enter assignees (comma-separated)",
    value="EKANEM, YAHYA, OKORO, EBOKA, PEREPUIGHE, SULEIMAN, KAREEM, AMEH, NURADEEN, ASUQUO, OLAEDO, AKINDUTIRE, ENEH, OKOYE, AKINSEFUNMI, GOZIE, PROMISE, TINUBU"
)
assignees = [a.strip() for a in assignees_input.split(",") if a.strip()]

# Save setup and move to next page
if st.button("Next: Configure Constraints"):
    if not shifts or not assignees:
        st.error("Please enter at least one shift type and one assignee.")
    else:
        st.session_state.start_date = str(start_date)
        st.session_state.end_date = str(end_date)
        st.session_state.shifts = shifts
        st.session_state.assignees = assignees
        st.session_state.setup_done = True
        st.success("Setup saved! Go to the Constraints page.")
