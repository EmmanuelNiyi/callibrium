import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
HTML_FILE = PROJECT_ROOT / "output_files" / "roster.html"

st.title("📊 Generated Schedule")

if HTML_FILE.exists():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    # full-width iframe
    components.html(html_content, height=800, width=None, scrolling=True)
else:
    st.info(f"No schedule found yet. Expected file at: {HTML_FILE}")
