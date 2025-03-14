import os
from webbrowser import get
import streamlit as st
import re
from PIL import Image
from create_email_account import create_user
from delete_email_account import delete_user
from delete_emails import delete_all_emails, delete_email
from getmail import get_emails

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def signup():
    st.title("Signup Page for gmail.com")
    email = st.text_input("Signup Email", placeholder="abc@gmail.com")
    password = st.text_input("Signup Password", type="password")
    if st.button("Signup"):
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif email.split('@')[1] != 'gmail.com':
            st.error("Incorrect SMTP server domain, please provide a valid gmail account.")
        else:
            result = create_user(email, password)

            if result.returncode != 0:
                st.error(f'Error: {result.stderr}')
                print(result.stderr)

            else:
                try:
                    emails = get_emails(email, password)
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = email
                    st.session_state["password"] = password
                    st.session_state["page"] = "Protected Page"
                    st.session_state["emails"] = emails
                except Exception as e:
                    st.error('Invalid email or password.')
            
    st.write("Already have an account?", unsafe_allow_html=True)
    if st.button("Go to Login"):
        st.session_state["page"] = "Login"
        st.rerun()

def login():
    st.title("Login Page for gmail.com")
    email = st.text_input("Login Email",placeholder="abc@gmail.com")
    password = st.text_input("Login Password", type="password")
    if st.button("Login"):
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif email.split('@')[1] != 'gmail.com':
            st.error("Incorrect SMTP server domain, please provide a valid gmail account.")
        else:
            try:
                emails = get_emails(email, password)
                st.session_state["authenticated"] = True
                st.session_state["user"] = email
                st.session_state["password"] = password
                st.session_state["page"] = "Protected Page"
                st.session_state["emails"] = emails
                st.rerun()
            except Exception as e:
                st.error('Invalid email or password.')
            
        
    if st.button("Go to Signup"):
        st.session_state["page"] = "Signup"
        st.rerun()

def protected_page():
    if not st.session_state.get("authenticated", False):
        st.warning("You must log in to access this page.")
        st.session_state["page"] = "Login"
        st.rerun()
    st.title("Protected Page")
    st.write(f"Welcome, {st.session_state['user']}!")
    emails = st.session_state["emails"]
    st.subheader("Your Emails")
    if emails:
        for idx, email in enumerate(emails, start=1):
            with st.expander(f"Email {idx + 1}"):
                st.write(email["text_result"])
                if email["attachment"]:
                    if os.path.exists(email["attachment"]):
                        image = Image.open(email["attachment"])
                        st.image(image, caption=f"Attachment for Email {idx}")
                    else:
                        st.write("Attachment not found.")
                else:
                    st.write("No attachment")
                if st.button(f"Delete Email {idx}", key=f"delete_email_{email['mail_id']}"):
                    delete_email(st.session_state["user"], st.session_state["password"], email["mail_id"])
                    st.rerun()
        if st.button("Delete All Emails"):
            delete_all_emails(st.session_state["user"], st.session_state["password"])
            st.rerun()
    else:
        st.write("No emails found.")
    


    if st.button("Logout"):
        st.session_state.clear()
        st.session_state["page"] = "Login"
        st.rerun()

    if st.button("Delete Account"):
        delete_user(st.session_state["user"])
        st.session_state.clear()
        st.session_state["page"] = "Login"
        st.rerun()

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Login"

    page = st.session_state["page"]

    if page == "Login":
        login()
    elif page == "Signup":
        signup()
    elif page == "Protected Page":
        protected_page()

if __name__ == "__main__":
    main()
