import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

uri = f"mongodb+srv://{username}:{password}@reactapp.0ltwq.mongodb.net/?retryWrites=true&w=majority&appName=ReactApp"
uri = uri.format(username, password)

def connect_to_db():
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        print("Connected to MongoDB")
        db = client["RAG_SUI"]
        chat_collection = db["Chats"]

        return chat_collection
    except Exception as e:
        print(e)