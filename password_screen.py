import streamlit as st

def render_password_screen():
    # 🔤 Inject custom CSS for Georgia font and centered layout
    st.markdown("""
        <style>
            html, body, [class*="css"] {
                font-family: Georgia, serif;
                text-align: center;
            }
            .welcome-text h1 {
                font-size: 38px;
                color: #d3d3d3;
                margin-bottom: 0;
            }
            .welcome-text h3 {
                margin-top: 5px;
                font-weight: normal;
                font-size: 20px;
            }
        </style>
        <div class='welcome-text'>
            <h1>Welcome to Dealer Management Systems</h1>
            <h3>Managed by: James Tobiasz<br>
                 Created and Coded by: Joshua R. Adams</h3>
        </div>
    """, unsafe_allow_html=True)

    st.image("assets/logo.jpeg", use_container_width=True) # Optional logo

    st.divider()

    password_input = st.text_input("🔑 Enter Password", type="password")

    # Load from secrets if available, fallback if not
    correct_password = st.secrets["correct_password"] if "correct_password" in st.secrets else "dealeradmin"

    if password_input:
        if password_input == correct_password:
            st.session_state.authenticated = True
            st.success("✅ Access granted. Redirecting...")
        else:
            st.error("❌ Incorrect password. Please try again.")