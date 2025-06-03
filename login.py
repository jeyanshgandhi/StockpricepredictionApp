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

# Function to check login credentials
def check_login(username, password):
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            # Query to check if the username and password match
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            return result is not None  # Returns True if the user is found
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
    return False

def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            if check_login(username, password):
                st.session_state.logged_in = True  # Set the login status to True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please enter both username and password.")
