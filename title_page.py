import streamlit as st
import pandas as pd
from tournament_parser import clean_raw_schedule

def render_title_page():
    # 🎨 Styling Block
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap');
            .stApp {
                background-color: #101010;
                font-family: 'EB Garamond', Georgia, serif;
                color: #d3d3d3;
                text-align: center;
            }
            h2 {
                font-size: 30px;
                color: #d3d3d3;
                margin-bottom: 5px;
            }
            .stFileUploader label {
                color: #c0c0c0 !important;
                font-size: 18px;
            }
        </style>
    """, unsafe_allow_html=True)

    # 🧭 Progress Tracker (Live status)
    st.markdown("### ✅ Progress Tracker")
    step_2_status = "✔️" if st.session_state.get("tournament_uploaded") else "⏳"
    step_3_status = "✔️" if st.session_state.get("ready_for_dashboard") else "⏳"
    st.markdown(f"""
        - ✔️ Step 1: Authenticated  
        - {step_2_status} Step 2: Upload Tournament File  
        - {step_3_status} Step 3: Confirm Tournament Preview  
    """)

    # 🏷️ Page Header
    st.markdown("<h2>Upload Tournament Excel File</h2>", unsafe_allow_html=True)

    # 📁 File Upload
    uploaded_file = st.file_uploader("Choose tournament file (.xlsx)", type=["xlsx"])

    if uploaded_file:
        try:
            raw_df = pd.read_excel(uploaded_file)
            with st.expander("🔬 Raw Sheet Preview: First 20 Rows"):
                st.write(raw_df.head(20))

            # 🧼 Clean and Store
            parsed_df = clean_raw_schedule(raw_df)
            st.session_state.tournament_uploaded = True
            st.session_state.parsed_df = parsed_df
            st.success("✅ Tournament file uploaded and cleaned.")

            # 🧠 Diagnostic Preview
            with st.expander("🧪 Raw Columns Before Cleaning"):
                st.write(raw_df.columns.tolist())

            with st.expander("🔍 Parsed Columns After Cleaning"):
                st.write(parsed_df.columns.tolist())

            with st.expander("👀 First 10 Raw Rows"):
                st.write(raw_df.head(10))

            # 🧮 Final Preview Setup
            preview_columns = [
                "Date",
                "Time",
                "Event Number",
                "Event Name",
                "Player Projection",
                "Dealer Forecast"
            ]

            st.subheader("📊 Preview Cleaned Tournament Data")
            st.dataframe(parsed_df[preview_columns])

            # ✅ User Confirmation Button
            if st.button("✅ Confirm & Proceed to Management Dashboard"):
                st.session_state.ready_for_dashboard = True
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error reading or parsing file: {str(e)}")