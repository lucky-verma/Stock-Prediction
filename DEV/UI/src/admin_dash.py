import streamlit as st

def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading About ..."):
        st.markdown(
            "## Admin\n"
            "This an open source project ")
