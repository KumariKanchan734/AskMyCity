import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
import sys

load_dotenv()
mongo_url = os.environ.get('MONGO_URL')

try:
    print("Connecting with pymongo...")
    # Explicitly provide CA bundle
    client = MongoClient(mongo_url, tlsCAFile=certifi.where())
    client.admin.command('ping')
    print("Ping success!")
except Exception as e:
    print(f"Error: {e}")
