
# users/mongodb_operations.py
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
from prometheus_client import Counter, Histogram

# Define Prometheus Metrics
MONGO_QUERY_COUNT = Counter(
    'mongodb_queries_total', 'Total MongoDB queries executed', ['collection', 'operation']
)
MONGO_QUERY_LATENCY = Histogram(
    'mongodb_query_latency_seconds', 'MongoDB query latency', ['collection', 'operation']
)

uri = "mongodb+srv://dbUser:dbUser@cluster0.xknwi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Connect to MongoDB (Make sure your MongoDB is running locally)
client = MongoClient(uri)
db = client['user_db']  # MongoDB database name
users_collection = db['users']  # MongoDB collection name

# CREATE: Insert a new user
def create_user(name: str):
    start_time = time.time()
    user = {"name": name}
    result = users_collection.insert_one(user)
    duration = time.time() - start_time
    MONGO_QUERY_COUNT.labels(collection="users", operation="create").inc()
    MONGO_QUERY_LATENCY.labels(collection="users", operation="create").observe(duration)
    return str(result.inserted_id)

# READ: Get a user by name
def get_user_by_name(name: str):
    return users_collection.find_one({"name": name})

# READ: Get a user by ID
def get_user_by_id(user_id: str):
    try:
        # Convert the string ID to ObjectId
        object_id = ObjectId(user_id)
        return users_collection.find_one({"_id": object_id})
    except Exception as e:
        # Handle invalid ObjectId or other errors
        print(f"Error: {e}")
        return None

# READ: Get all users
def get_all_users():
    return list(users_collection.find())

# UPDATE: Update an existing user's name
def update_user(user_id: str, new_name: str):
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": new_name}})
    return result.modified_count > 0

# DELETE: Delete a user by name
def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
