import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import sys

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Load env from current directory
load_dotenv()

mongo_url = os.environ.get('MONGO_URL')
if not mongo_url:
    print("MONGO_URL not found in environment!")
    sys.exit(1)

print(f"Attempting to connect with Motor...")

import certifi

async def test():
    try:
        # Explicitly provide CA bundle
        logging.info(f"Using CA bundle from: {certifi.where()}")
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
        logging.info("Client created with explicit CA. sending ping...")
        # Force a connection
        await client.admin.command('ping')
        logging.info("Ping successful! Database connection is working.")
    except Exception as e:
        logging.error(f"Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(test())
    except Exception as e:
        print(f"Script execution failed: {e}")
