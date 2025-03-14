import streamlit as st

# Simulated user database
USER_CREDENTIALS = {}

def signup():
    st.title("Signup Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        if username in USER_CREDENTIALS:
            st.error("Username already exists!")
        else:
            USER_CREDENTIALS[username] = password
            st.success("Signup successful! Please login.")
            st.switch_page("login")

def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["user"] = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def protected_page():
    if not st.session_state.get("authenticated", False):
        st.warning("You must log in to access this page.")
        st.stop()
    st.title("Protected Page")
    st.write(f"Welcome, {st.session_state['user']}!")
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Signup", "Protected Page"])
    
    if page == "Login":
        login()
    elif page == "Signup":
        signup()
    elif page == "Protected Page":
        protected_page()

if __name__ == "__main__":
    main()
