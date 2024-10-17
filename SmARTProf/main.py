import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")

my_db = my_client["smartprof"]

users_collection = my_db['users']

# Test the connection by inserting a sample document
sample_user = {"username": "testuser", "password": "password123"}
result = users_collection.insert_one(sample_user)
print(f"Inserted user with ID: {result.inserted_id}")
