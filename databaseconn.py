import mysql.connector
from mysql.connector import Error
import streamlit as st

# Database connection
import mysql.connector

import mysql.connector

def create_connection():
    try:
        # Attempt to create connection
        conn = mysql.connector.connect(
            host="ba-dev-01.cbz7aitzqkud.us-east-1.rds.amazonaws.com",  # RDS endpoint
            user="migue",       # MySQL username
            password="migue0627",  # MySQL password
            database="fitness_app"  # Database schema
        )
        if conn.is_connected():
            print("Connected to MySQL server")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Function to get all laptops from the laptops_data table
def get_laptops():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT product_id, Manufacturer, Category, Price FROM laptops_data")
    laptops = cursor.fetchall()
    cursor.close()
    conn.close()
    return laptops

# Function to insert an order into orders_data
def create_order(customer_id, product_id, price):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders_data (customer_id, customer_name, product_id, product_price, order_date)
        SELECT c.customer_id, CONCAT(c.first_name, ' ', c.last_name), l.product_id, l.Price, CURDATE()
        FROM customers_data c
        JOIN laptops_data l ON l.product_id = %s
        WHERE c.customer_id = %s
    """, (product_id, customer_id))
    conn.commit()
    st.success("Order placed successfully!")
    cursor.close()
    conn.close()
