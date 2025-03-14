import io
import os
import streamlit as st
import re
from PIL import Image
from create_email_account import create_user
from delete_email_account import delete_user
from delete_emails import delete_all_emails, delete_email
from getmail import get_emails
from sendmail import send_email

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

            else:
                try:
                    emails = get_emails(email, password)  #to check if user exists and we are successfully able to retrieve their emails, only then we can log them in
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = email
                    st.session_state["password"] = password
                    st.session_state["page"] = "Home Page"
                except Exception as e:
                    st.error('Invalid email or password.')
                st.rerun()
            
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
                st.session_state["page"] = "Home Page"
                st.rerun()
            except Exception as e:
                st.error(f'Error logging in: {e}')
            
        
    if st.button("Go to Signup"):
        st.session_state["page"] = "Signup"
        st.rerun()

def protected_page():
    if not st.session_state.get("authenticated", False):
        st.warning("You must log in to access this page.")
        st.session_state["page"] = "Login"
        st.rerun()
    st.title("Inbox")
    st.write(f"Welcome, {st.session_state['user']}!")
    emails = get_emails(st.session_state["user"], st.session_state["password"])
    if st.button("Compose Email"):
        st.session_state["page"] = "Compose Email"
        st.rerun()

    st.subheader("Emails Received:")
    if emails:
        for idx, email in enumerate(emails, start=1):
            with st.expander(email["subject"] or email["body"][:20] + '...' if len(email["body"]) > 20 else email["body"]):
                st.write(f'From: {email["from"]}')
                if email["subject"]:
                    st.write(f'Subject: {email["from"]}')
                else:
                    st.write(f'No Subject')
                st.write(f'Body: {email["body"]}')
                if email["attachment"]:
                    if os.path.exists(email["attachment"]):
                        image = Image.open(email["attachment"])
                        st.image(image, caption=f"Attachment of Email {idx}")
                    else:
                        st.write("Attachment not found.")
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


def compose_email_page():
    if not st.session_state.get("authenticated", False):
        st.warning("You must log in to access this page.")
        st.session_state["page"] = "Login"
        st.rerun()
    st.title("Compose Email")

    recepient = st.text_input("To",placeholder="abc@gmail.com")
    subject = st.text_input("Subject")
    # Text input for email content
    email_content = st.text_area("Email Content", "", height=200)

    # File uploader for optional image attachment
    attachment = st.file_uploader("Attach an image (optional)")
    
        
    if attachment is not None:
        try:
            image = Image.open(attachment)
            st.image(image, caption="Selected Image", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")

    # Send button
    if st.button("Send"):
        if email_content.strip() == "":
            st.error("Email content cannot be empty.")
        else:
            # Process the email content and attachment as needed
            try:
                send_email(st.session_state["user"], recepient, subject, email_content, attachment) 
                print("Email sent successfully")     
            except Exception as e:
                st.error(f'Error sending email: {e}')

            # Redirect back to the Home Page
            st.session_state["page"] = "Home Page"
            st.rerun()
    # Cancel button
    if st.button("Cancel"):
            st.session_state["page"] = "Home Page"
            st.rerun()

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Login"

    page = st.session_state["page"]

    if page == "Login":
        login()
    elif page == "Signup":
        signup()
    elif page == "Home Page":
        protected_page()
    elif st.session_state["page"] == "Compose Email":
        compose_email_page()

if __name__ == "__main__":
    main()
