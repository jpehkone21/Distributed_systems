'''
from pymongo import MongoClient

# Connect to the MongoDB server (local server or remote)
uri = "mongodb+srv://dbUser:dbUser@cluster0.xknwi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)  # Update the URI if you're using MongoDB Atlas
db = client["user_db"]  # Create (or use) a database called "user_db"
users_collection = db["users"]  # Create (or use) a collection called "users"

# Function to create a new user in MongoDB
def create_user(name):
    user = {"name": name}
    result = users_collection.insert_one(user)  # Insert the user into the "users" collection
    return result.inserted_id

# Function to find a user in MongoDB by name
def find_user(name):
    return users_collection.find_one({"name": name})
'''