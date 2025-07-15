import streamlit as st
import password_screen
import title_page
import workspace  # Placeholder for future tabs

def render_active_tab(tab_name):
    if tab_name == "Tournament Forecast":
        from tabs.schedule_management import render_schedule_tab
        render_schedule_tab()

    elif tab_name == "Employee Management":
        from tabs.employee_management import render_employee_tab
        render_employee_tab()

    elif tab_name == "Carpool Coordination":
        from tabs.carpool_management import render_carpool_tab
        render_carpool_tab()

    elif tab_name == "Uniform Return":
        from tabs.uniform_return import render_uniform_tab
        render_uniform_tab()

    elif tab_name == "Dealer Demand Heatmap":
        from tabs.heatmap_dashboard import render_heatmap_tab
        render_heatmap_tab()

    elif tab_name == "Roll Call Sheet":
        from tabs.rollcall_sheet import render_rollcall_tab
        render_rollcall_tab()

    elif tab_name == "Schedule Generator":
        from tabs.schedule_generator import render_schedulegen_tab
        render_schedulegen_tab()

    elif tab_name == "Manual Employee Entry":
        from tabs.manual_employee_builder import render_manual_employee_tab
        render_manual_employee_tab()

# 🎨 Global Styling: Background + Font
st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            font-family: Georgia, serif;
            color: #000000;
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
st.session_state.setdefault("active_module", "Tournament Forecast")
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
    title_page.render_title_page()

else:
    # 🧭 Sidebar Navigation
    tab = st.sidebar.selectbox("🧭 Choose View:", [
        "Tournament Forecast",
        "Employee Management",
        "Carpool Coordination",
        "Schedule Generator",
        "Manual Employee Entry"
    ])
    st.session_state.active_module = tab

    # 🎛️ Dynamic Sidebar Filters
    st.sidebar.markdown("---")

    if tab == "Tournament Forecast":
        st.sidebar.markdown("### 🎯 Forecast Filters")
        st.sidebar.radio("View Mode", ["Daily", "Missing Projections", "By Format"], key="forecast_view")
        st.sidebar.selectbox("Shift Filter", ["All Shifts", "AM", "PM"], key="shift_filter")
        st.sidebar.selectbox("Game Format", ["Holdem", "Mixed", "Restarts"], key="game_format")

    elif tab == "Employee Management":
        st.sidebar.markdown("### 👥 Employee Controls")
        st.sidebar.radio("Action", ["Lookup", "Add", "Edit", "Swap Shifts"], key="employee_action")
        st.sidebar.selectbox("Shift Preference", ["Any", "AM", "PM"], key="employee_shift_pref")

    elif tab == "Carpool Coordination":
        st.sidebar.markdown("### 🚗 Carpool Filters")
        st.sidebar.selectbox("View Mode", ["Drivers", "Riders", "Unassigned"], key="carpool_view")

    # ⛳ Tab Renderer – now scoped correctly
    render_active_tab(tab)