import pandas as pd
import pymongo

# MongoDB connection
client = pymongo.MongoClient(f'mongodb+srv://xchmcr:Waffletea27@clustertest01.dc3gd.mongodb.net/')
db = client["laptopsappdatabase"]  # Replace with your database name
laptops_collection = db["laptopsappcollection"]  # Replace with your collection name

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(r'C:\Users\Migue\csvtomysqlattempt\laptops.csv')  # Replace with the path to your CSV file

# Convert the DataFrame to a list of dictionaries (which MongoDB accepts)
laptops_dict = df.to_dict("records")

# Insert the data into the MongoDB collection
laptops_collection.insert_many(laptops_dict)

print("CSV data inserted successfully into MongoDB!")
