import pymongo

def connect_to_mongo():
    # MongoDB connection
    client = pymongo.MongoClient(f'mongodb+srv://xchmcr:Waffletea27@clustertest01.dc3gd.mongodb.net/')
    db = client["laptopsappdatabase"]  # Replace with your database name
    return db
