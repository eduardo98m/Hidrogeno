import streamlit as st
from pathlib import Path


def display_paper():
    st.markdown(
        Path("paper.md").read_text(encoding="utf-8"),
        unsafe_allow_html=True
    )
    