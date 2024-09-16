import streamlit as st
from databaseconn import create_connection  # Previously 'database'

# Sign up newppl
def sign_up_user(first_name, last_name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers_data WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    if user:
        st.error("Email already exists, please log in.")
    else:
        cursor.execute("""
            INSERT INTO customers_data (first_name, last_name, email)
            VALUES (%s, %s, %s)
        """, (first_name, last_name, email))
        conn.commit()
        st.success("Account created successfully! Please log in.")
    cursor.close()
    conn.close()

# Log in users
def login_user(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers_data WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        st.session_state['user'] = {
            'customer_id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'email': user[3]
        }
        st.success(f"Logged in as {user[1]} {user[2]}")
        return True
    else:
        st.error("Email not found. Please sign up.")
        return False
