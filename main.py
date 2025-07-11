import streamlit as st
import password_screen
import title_page
import workspace  # Placeholder for future tabs

# 🎨 Global Styling: Background + Font
st.markdown("""
    <style>
        .stApp {
            background-color: #101010;
            font-family: Georgia, serif;
            color: #d3d3d3;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #e0e0e0;
        }
        .stTextInput > label {
            color: #c0c0c0 !important;
        }
        .stButton button {
            background-color: #d3d3d3;
            color: black;
        }
        .stDivider {
            border-top: 1px solid #555555;
        }
    </style>
""", unsafe_allow_html=True)

# 🔒 Ensure session flags exist
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("tournament_uploaded", False)
st.session_state.setdefault("ready_for_dashboard", False)
st.session_state.setdefault("dealer_initialized", False)

# 🚦 Route the flow
if not st.session_state.authenticated:
    password_screen.render_password_screen()

elif not st.session_state.tournament_uploaded:
    title_page.render_title_page()

elif not st.session_state.ready_for_dashboard:
    # Visual step tracker on Title Page Confirmation
    st.markdown("### ✅ Progress Tracker")
    st.markdown("""
        - ✔️ Step 1: Authenticated  
        - ✔️ Step 2: Tournament File Uploaded  
        - ⏳ Step 3: Confirm Tournament Preview  
    """)
    title_page.render_title_page()

else:
    # 🧭 Sidebar Navigation
    tab = st.sidebar.selectbox("🧭 Choose View:", [
        "Tournament Forecast",
        "Employee Management",
        "Carpool Coordination"
    ])

    if tab == "Tournament Forecast":
        from tabs.schedule_management import render_schedule_tab
        render_schedule_tab()

    elif tab == "Employee Management":
        from tabs.employee_management import render_employee_tab
        render_employee_tab()

    elif tab == "Carpool Coordination":
        from tabs.carpool_management import render_carpool_tab
        render_carpool_tab()