import streamlit as st

# --- Page configuration ---
st.set_page_config(
    page_title="Modular Schedule Generator",
    page_icon="🗓️",
    layout="centered"
)

# --- Header ---
st.title("🗓️ Modular Schedule Generator")
st.write("""
Welcome! This app helps you create **fair and flexible schedules** for multiple shifts and assignees.
""")

# --- Key Features ---
st.markdown("### ✨ Key Features")
st.markdown("""
- Generate schedules for **any date range**, including weekends.  
- Handle **multiple shift types** per day (e.g., Ward, Emergency).  
- Ensure **fair distribution** of shifts among all assignees.  
- Export schedules as **CSV or HTML** for easy use.
""")

# --- Workflow ---
st.markdown("### 🏁 How to Use")
st.markdown("""
1. Go to the **Input Page** to enter your information.  
2. Run the schedule generation on the **Run Script Page**.  
3. View and download your schedule on the **Results Page**.
""")

# --- Large “Start” Button Styled as Link ---
st.markdown("---")
st.markdown(
    """
<p style="text-align:center;">
    <a href="/setup" style="
        display:inline-block;
        background-color:#4CAF50;
        color:white;
        padding:15px 40px;
        font-size:22px;
        font-weight:bold;
        border-radius:10px;
        text-decoration:none;">
        🚀 Start Here
    </a>
</p>
""",
    unsafe_allow_html=True
)
