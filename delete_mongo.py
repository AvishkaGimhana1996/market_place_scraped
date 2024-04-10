from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Select the database and collection
db = client['market_place_scraped_data']
collection = db['post_data']

# Delete all records from the collection
result = collection.delete_many({})

# Print the number of deleted documents
print(f"Deleted {result.deleted_count} documents")

