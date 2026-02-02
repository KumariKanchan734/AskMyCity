import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
import sys

load_dotenv()
mongo_url = os.environ.get('MONGO_URL')

try:
    print("Connecting with pymongo (INSECURE)...")
    # Disable SSL verification
    client = MongoClient(mongo_url, tlsAllowInvalidCertificates=True)
    client.admin.command('ping')
    print("Ping success (INSECURE)!")
except Exception as e:
    print(f"Error: {e}")
