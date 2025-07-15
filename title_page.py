import streamlit as st
import pandas as pd
from tournament_parser import clean_raw_schedule

def render_title_page():
    # 🎨 Styling Block — Light mode
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap');
            .stApp {
                background-color: #FFFFFF;
                font-family: 'EB Garamond', Georgia, serif;
                color: #000000;
            }
            h2 {
                font-size: 30px;
                color: #000000;
                margin-bottom: 5px;
                text-align: center;
            }
            .stFileUploader label {
                color: #333333 !important;
                font-size: 18px;
            }
        </style>
    """, unsafe_allow_html=True)

    # 🏷️ Header & Guidance
    st.markdown("<h2>Import Page</h2>", unsafe_allow_html=True)
    st.caption("""
        • Upload Tournament List as-is (after deleting first three rows) to preview.<br>
        • Upload the most recent Dealer Master List or generate one under <i>View → Dealer Entry</i>.<br>
        • Upload most recent Employee Schedule (Coming Soon).<br>
        • Supported formats: .xlsx and .csv
    """, unsafe_allow_html=True)
    st.divider()

    # 📁 Tournament Upload
    st.subheader("📁 Tournament Schedule Upload")
    tournament_file = st.file_uploader("Upload Tournament (.xlsx or .csv)", type=["xlsx", "csv"], key="tournament_file")

    if tournament_file:
        try:
            ext = tournament_file.name.split(".")[-1].lower()
            raw_df = pd.read_excel(tournament_file) if ext == "xlsx" else pd.read_csv(tournament_file)
            parsed_df = clean_raw_schedule(raw_df)

            # 📅 Normalize and tag weekday
            parsed_df["Date"] = pd.to_datetime(parsed_df["Date"], errors="coerce")
            parsed_df["Weekday"] = parsed_df["Date"].dt.day_name()

            st.session_state.tournament_uploaded = True
            st.session_state.parsed_df = parsed_df

            st.success("✅ Tournament file uploaded and cleaned.")
            st.dataframe(parsed_df[[
                "Date", "Weekday", "Time", "Event Number",
                "Event Name", "Player Projection", "Dealer Forecast"
            ]], use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error parsing tournament file: {e}")

    st.divider()

    # 📘 Dealer Master Import
    st.subheader("📘 Dealer Master List Upload")
    dealer_file = st.file_uploader("Upload dealer_master_list (.xlsx or .csv)", type=["xlsx", "csv"], key="dealer_master")

    if dealer_file:
        try:
            ext = dealer_file.name.split(".")[-1].lower()
            dealer_df = pd.read_excel(dealer_file) if ext == "xlsx" else pd.read_csv(dealer_file)

            required_cols = [
                "first_name", "last_name", "nametag_id", "ee_number", "email", "phone",
                "ft_pt", "dealer_group"
            ] + [f"AVAIL-{day}" for day in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]]

            missing = [col for col in required_cols if col not in dealer_df.columns]
            if missing:
                st.error(f"❌ Missing columns: {missing}")
            else:
                st.session_state.dealer_master_list = dealer_df
                st.success(f"✅ Imported {len(dealer_df)} dealers successfully.")
                st.dataframe(dealer_df.head(20), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error parsing dealer file: {e}")

    st.divider()

    # 🗓️ Employee Schedule Upload (Staged)
    st.subheader("🗓️ Employee Schedule Upload (Coming Soon)")
    schedule_file = st.file_uploader("Upload employee schedule (.xlsx or .csv)", type=["xlsx", "csv"], key="emp_schedule")
    if schedule_file:
        st.info("📌 Schedule upload staged. Parsing logic not yet implemented.")

    st.divider()

    # 🚀 Navigation
    st.markdown("### ✅ Ready to proceed?")
    if st.button("Proceed to Management Dashboard"):
        st.session_state.ready_for_dashboard = True
        st.rerun()