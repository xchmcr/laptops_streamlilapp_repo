from databaseconn import connect_to_mongo

# Function to sign up a new user
def sign_up_user(first_name, last_name, email):
    db = connect_to_mongo()
    users_collection = db["users_data"]  # Name of the MongoDB collection for users

    # Insert new user into MongoDB
    new_user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }
    users_collection.insert_one(new_user)
    return "User registered successfully!"

# Function to log in an existing user
def login_user(email):
    db = connect_to_mongo()
    users_collection = db["users_data"]

    # Find the user by email in MongoDB
    user = users_collection.find_one({"email": email})
    if user:
        return user
    return None
