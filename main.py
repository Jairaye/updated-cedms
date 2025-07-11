import streamlit as st
import password_screen
import title_page
import workspace  # Placeholder for future tabs

# 🎨 Global Styling: Background + Font
st.markdown("""
    <style>
        .stApp {
            background-color: #101010;  /* Deep black background */
            font-family: Georgia, serif;
            color: #d3d3d3;  /* Silver text */
        }

        h1, h2, h3, h4, h5, h6 {
            color: #e0e0e0;  /* Lighter silver for headers */
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

# 🔒 Ensure session auth flag exists
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 🧠 Session flags for data availability
st.session_state.setdefault("tournament_uploaded", False)
st.session_state.setdefault("dealer_initialized", False)

# 🚦 Route the flow
if not st.session_state.authenticated:
    password_screen.render_password_screen()

elif not st.session_state.tournament_uploaded:
    title_page.render_title_page()

else:
    workspace.render_workspace()  # Replace with actual workspace content