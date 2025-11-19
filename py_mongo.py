from bson import ObjectId
from pymongo import MongoClient  # pip install pymongo

client = MongoClient(host="localhost", port= 27018, username="mongoadmin", password="bdung")  # need mongo server running with this configuration

def get_collection():
    """
    Connect to MongoDB and return a collection handle.
    Adjust the URI, DB name, and collection name as needed.
    """
    db = client["my_database"]
    collection = db["users"]
    return collection


def create_user(name: str, email: str, age: int) -> str:
    """
    Insert a new user document into the collection.
    Returns the inserted document's ID as a string.
    """
    collection = get_collection()
    doc = {
        "name": name,
        "email": email,
        "age": age,
    }
    result = collection.insert_one(doc)
    return str(result.inserted_id)

def get_user_by_id(user_id: str) -> dict | None:
    """
    Find a single user by its _id.
    Returns the document as a dict, or None if not found.
    """
    collection = get_collection()
    doc = collection.find_one({"_id": ObjectId(user_id)})
    return doc

def get_user_by_name(name: str) -> dict | None:
    collection = get_collection()
    doc = collection.find_one({"name": name})
    return doc

def get_users_by_min_age(min_age: int) -> list[dict]:
    """
    Find all users with age >= min_age.
    Returns a list of documents.
    """
    collection = get_collection()
    cursor = collection.find({"age": {"$gte": min_age}})
    return list(cursor)

def update_user_email(name: str, new_email: str) -> int:
    """
    Update a user's email by _id.
    Returns the number of modified documents (0 or 1).
    """
    collection = get_collection()
    # update users set email=__new_email__ where name==__name__
    result = collection.update_one(
        {"name": name},
        {"$set": {"email": new_email}}
    )
    return result.modified_count

def increase_age_for_all(min_age: int, increment: int) -> int:
    """
    Increase age by `increment` for all users with age >= min_age.
    Returns the number of modified documents.
    """
    collection = get_collection()
    result = collection.update_many(
        {"age": {"$gte": min_age}},
        {"$inc": {"age": increment}}
    )
    return result.modified_count


def delete_user(user_id: str) -> int:
    """
    Delete a user by _id.
    Returns the number of deleted documents (0 or 1).
    """
    collection = get_collection()
    result = collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count


def delete_users_younger_than(max_age: int) -> int:
    """
    Delete all users with age < max_age.
    Returns the number of deleted documents.
    """
    collection = get_collection()
    result = collection.delete_many(   {"age": {"$lt": 40}  }   )
    return result.deleted_count

col = get_collection()

# Clean collection for demo
col.delete_many({})

print("=== CREATE ===")
user1_id = create_user("Alice", "alice@example.com", 25)
user2_id = create_user("Bob", "bob@example.com", 30)
print("Inserted Alice with _id:", user1_id)
print("Inserted Bob with _id:", user2_id)

print("\n=== READ ===")
user1 = get_user_by_id(user1_id)
print("User 1:", user1)
user1 = get_user_by_name("Alice")
print("User 1:", user1)

print('users older equal 23 age')
for i, user in enumerate(get_users_by_min_age(23)):
    print(f' #{i+1} ', user)

print("\n=== UPDATE ===")
modified = update_user_email('Alice', "alice.new@example.com")
print("Modified docs:", modified)
print("Alice after email update:", get_user_by_id(user1_id))
