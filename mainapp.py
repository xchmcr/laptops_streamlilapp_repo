import streamlit as st
from user_management import sign_up_user, login_user  
from databaseconn import get_laptops, create_order
def main():
    st.title("Laptop Store")

    # Sign-up/Login selection
    if 'user' not in st.session_state:
        st.sidebar.title("Login / Sign Up")
        login_choice = st.sidebar.radio("Do you have an account?", ["Log In", "Sign Up"])

        if login_choice == "Sign Up":
            first_name = st.sidebar.text_input("First Name")
            last_name = st.sidebar.text_input("Last Name")
            email = st.sidebar.text_input("Email")

            if st.sidebar.button("Sign Up"):
                if first_name and last_name and email:
                    sign_up_user(first_name, last_name, email)
                else:
                    st.error("Please fill out all fields.")

        elif login_choice == "Log In":
            email = st.sidebar.text_input("Email")

            if st.sidebar.button("Log In"):
                if email:
                    login_user(email)
                else:
                    st.error("Please enter your email.")

    else:
        st.sidebar.success(f"Logged in as {st.session_state['user']['first_name']}")

        # retrieve laptop options
        laptops = get_laptops()
        if laptops:
            st.write("### Available Laptops")
            st.table(laptops)

            # select a product to buy
            product_selection = st.selectbox(
                "Select a Laptop to Purchase",
                options=[(laptop['product_id'], laptop['Manufacturer'], laptop['Price']) for laptop in laptops],
                format_func=lambda x: f"{x[1]} - ${x[2]}"
            )

            if st.button("Buy Now"):
                create_order(
                    customer_id=st.session_state['user']['customer_id'],
                    product_id=product_selection[0],
                    price=product_selection[2]
                )

if __name__ == "__main__":
    main()
