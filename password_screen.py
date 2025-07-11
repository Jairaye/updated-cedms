import streamlit as st

def render_password_screen():
    # 🎨 Inject custom CSS: Garamond font, layout, and silver styling
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=EB+Garamond&display=swap');

            html, body, [class*="css"] {
                font-family: 'EB Garamond', Georgia, serif;
                text-align: center;
                background-color: #101010;
                color: #d3d3d3;
            }

            .welcome-text h1 {
                font-size: 38px;
                color: #d3d3d3;
                margin-bottom: 0;
                font-weight: 600;
            }

            .welcome-text h3 {
                margin-top: 5px;
                font-weight: normal;
                font-size: 20px;
            }

            .stTextInput > label {
                color: #c0c0c0 !important;
                font-weight: 500;
            }

            .stButton button {
                background-color: #d3d3d3;
                color: #101010;
                font-weight: 600;
            }
        </style>

        <div class='welcome-text'>
            <h1>Welcome to Dealer Management Systems</h1>
            <h3>Managed by: James Tobiasz<br>
                 Created and Coded by: Joshua R. Adams</h3>
        </div>
    """, unsafe_allow_html=True)

    # 🖼️ Logo
    st.image("assets/logo.jpeg", use_container_width=True)

    st.divider()

    # 🔐 Password input
    password_input = st.text_input("🔑 Enter Password", type="password")

    # ✅ Load password from secrets with fallback
    correct_password = st.secrets["correct_password"] if "correct_password" in st.secrets else "dealeradmin"

    if password_input:
        if password_input == correct_password:
            st.session_state.authenticated = True
            st.success("✅ Access granted. Redirecting...")
            st.rerun()
        else:
            st.error("❌ Incorrect password. Please try again.")