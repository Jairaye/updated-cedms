import streamlit as st
from tournament_parser import forecast_dealers

# 🎨 Styling
st.markdown("""
    <style>
        div[data-baseweb="select"] label {
            color: #ffffff !important;
            font-weight: 500;
        }
        .stDataFrame td {
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

def render_schedule_tab():
    st.title("🧮 Tournament Forecast")

    df = st.session_state.get("parsed_df")
    if df is None:
        st.warning("No tournament data found.")
        return

    # ✅ Init tracking column
    if "User_Edited" not in df.columns:
        df["User_Edited"] = False

    # 📅 Day Selector
    available_days = sorted(df["Date"].dropna().unique())
    selected_day = st.selectbox("📆 Choose a Day to View", available_days)

    # 🔁 Restart Filter
    restart_mode = st.radio(
        "🔄 Filter by Restart Status",
        ["Show All", "Only Restarts", "Only Non-Restarts"]
    )

    # ⚠️ Missing Projections Filter
    show_missing_only = st.checkbox("⚠️ Show Events Missing Player Projection")

    # 🔍 Filter logic
    filtered_df = df[df["Date"] == selected_day]

    if restart_mode == "Only Restarts":
        filtered_df = filtered_df[filtered_df["Restart_Flag"] == True]
    elif restart_mode == "Only Non-Restarts":
        filtered_df = filtered_df[filtered_df["Restart_Flag"] == False]

    if show_missing_only:
        filtered_df = filtered_df[filtered_df["Player Projection"] == 0]

    # ✏️ Projection Editor
    with st.expander(f"📋 Edit Player Projections for {selected_day.strftime('%B %d')}"):
        if filtered_df.empty:
            st.info("🎯 No events match this filter.")
        else:
            for i, row in filtered_df.iterrows():
                st.markdown(f"**Event #{row['Event Number']} – {row['Event Name']}**")
                new_projection = st.number_input(
                    f"Player Projection (was {row['Player Projection']})",
                    min_value=0,
                    value=row['Player Projection'],
                    key=f"proj_{i}"
                )
                if new_projection != row['Player Projection']:
                    df.at[i, "Player Projection"] = new_projection
                    df.at[i, "Dealer Forecast"] = forecast_dealers(new_projection, row["Handed"])
                    df.at[i, "User_Edited"] = True
                    st.success("✅ Updated dealer forecast")

    # 💾 Edited Summary Expander
    edited_rows = df[df["User_Edited"] == True]

    with st.expander("💾 Summary of Edited Events (Needs Save)"):
        if edited_rows.empty:
            st.info("No manual edits yet.")
        else:
            save_cols = [
                "Date", "Time", "Event Number", "Event Name",
                "Player Projection", "Dealer Forecast", "User_Edited"
            ]
            st.dataframe(edited_rows[save_cols])

            # 🔘 Save button to commit to session state
            if st.button("✅ Save Updates to Session"):
                st.session_state.parsed_df = df
                st.success("Saved changes to current session.")

    # 📊 Final Forecast Table
    view_columns = [
        "Date", "Time", "Event Number", "Event Name",
        "Player Projection", "Dealer Forecast", "Restart_Flag", "User_Edited"
    ]
    st.subheader("📊 Filtered Forecast View")
    st.dataframe(filtered_df[view_columns])