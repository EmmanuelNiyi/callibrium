import sys
import os

# Add the project root to sys.path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if repo_root not in sys.path:
    sys.path.append(repo_root)

from core.solver import main  # now it works
import streamlit as st

st.title("Run Scheduler Solver")

if st.button("Run Solver"):
    with st.spinner("Solver is running..."):
        result = main()
    st.success("Solver finished!")
    st.write("Result:", result)
