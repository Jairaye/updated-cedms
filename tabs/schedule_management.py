import streamlit as st

def render_schedule_tab():
    st.title("🧮 Tournament Forecast")
    df = st.session_state.get("parsed_df")
    if df is not None:
        st.dataframe(df)  # Later you'll group and visualize here
    else:
        st.warning("No tournament data found.")