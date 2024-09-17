import streamlit as st
from user_management import sign_up_user, login_user
from databaseconn import connect_to_mongo
import pandas as pd

def main():
    st.title("Laptops Ordering System")

    # Session state to track logged-in status
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "customer_id" not in st.session_state:
        st.session_state.customer_id = None

    # Display different menu options based on login status
    if st.session_state.logged_in:
        menu = ["Place Order", "Log Out"]  # Only show "Place Order" if logged in
    else:
        menu = ["Sign Up", "Log In"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Sign Up":
        st.subheader("Create New Account")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")

        if st.button("Sign Up"):
            message = sign_up_user(first_name, last_name, email)
            st.success(message)

    elif choice == "Log In":
        st.subheader("Log In")
        email = st.text_input("Email")
        if st.button("Log In"):
            user = login_user(email)
            if user:
                st.success(f"Welcome {user['first_name']} {user['last_name']}")
                st.session_state.logged_in = True
                st.session_state.customer_id = user["_id"]  # Save user ID in session

                # Instead of rerunning, show the interface directly
                place_order_interface(st.session_state.customer_id)
            else:
                st.error("User not found, please sign up first.")

    elif choice == "Place Order":
        if st.session_state.logged_in:  # Double-check login state
            place_order_interface(st.session_state.customer_id)
        else:
            st.error("Please log in first.")

    elif choice == "Log Out":
        st.session_state.logged_in = False
        st.session_state.customer_id = None
        st.success("Logged out successfully!")

def place_order_interface(customer_id):
    st.subheader("Place an Order")

    db = connect_to_mongo()
    laptops_collection = db["laptopsappcollection"]

    # Get list of laptops from MongoDB to display with more details
    laptops = list(laptops_collection.find({}, {"_id": 0, "product_id": 1, "Manufacturer": 1, "Screen_Size_inch": 1, "RAM_GB": 1, "Storage_GB_SSD": 1, "Price": 1}))

    # Create a dictionary with concatenated details as keys and product_id as values
    laptop_options = {f"{laptop['Manufacturer']} - {laptop['Screen_Size_inch']}\" - {laptop['RAM_GB']}GB RAM - {laptop['Storage_GB_SSD']}GB SSD - ${laptop['Price']}": laptop["product_id"] for laptop in laptops}

    if laptop_options:
        selected_laptop = st.selectbox("Select a Laptop", list(laptop_options.keys()), key="laptop_selectbox")
        laptop_id = laptop_options[selected_laptop]

        if st.button("Place Order"):
            order_status = place_order(customer_id, laptop_id)
            st.success(order_status)
    else:
        st.warning("No laptops available for ordering at the moment.")


def place_order(customer_id, laptop_id):
    db = connect_to_mongo()
    laptops_collection = db["laptopsappcollection"]
    orders_collection = db["orders_data"]

    # Find the laptop by product_id
    laptop = laptops_collection.find_one({"product_id": laptop_id})
    
    if laptop:
        order = {
            "customer_id": customer_id,
            "laptop_id": laptop_id,
            "price": laptop["Price"],  # Corrected to "Price" (capital P)
            "purchase_date": pd.Timestamp.now()
        }
        orders_collection.insert_one(order)
        return "Order placed successfully!"
    else:
        return "Laptop not found!"

if __name__ == "__main__":
    main()
