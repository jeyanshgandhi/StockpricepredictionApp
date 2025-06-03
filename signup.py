import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            database='stock_app',  # Use your database name
            user='root',  
            password='kakabapa12'  # Your MySQL password
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to insert user details into the database
def insert_user(username, password):
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            # Insert user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            st.success("Sign up successful! You can now log in.")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def signup():
    st.title("Sign Up Page")
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")

    if st.button("Sign Up"):
        if username and password:
            # Insert user details into the database
            insert_user(username, password)
            st.session_state.sign_up_completed = True  # Mark signup as completed
        else:
            st.error("Please enter both username and password.")

    # Add a button for users who already have an account
    if st.button("Already have an account? Log In"):
        st.session_state.sign_up_completed = True  # Redirect to login page by marking sign-up as completed
