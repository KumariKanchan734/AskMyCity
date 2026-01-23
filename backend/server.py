from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class City(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    name: str
    slug: str

class Service(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    city_slug: str
    service_type: str
    contact: str
    description: str

class CityWithServices(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    name: str
    slug: str
    services: List[Service]


# Seed database with initial data
async def seed_database():
    """
    Pre-populate the database with cities and services if they don't exist
    """
    # Check if cities already exist
    cities_count = await db.cities.count_documents({})
    
    if cities_count == 0:
        # Insert cities
        cities_data = [
            {"name": "Delhi", "slug": "delhi"},
            {"name": "Mumbai", "slug": "mumbai"},
            {"name": "Bangalore", "slug": "bangalore"}
        ]
        await db.cities.insert_many(cities_data)
        
        # Insert services for each city
        services_data = [
            # Delhi services
            {"city_slug": "delhi", "service_type": "Emergency", "contact": "112", "description": "National Emergency Number for all emergencies"},
            {"city_slug": "delhi", "service_type": "Hospital", "contact": "102", "description": "CATS Ambulance Service - 24/7 emergency medical assistance"},
            {"city_slug": "delhi", "service_type": "Police", "contact": "100", "description": "Delhi Police Emergency Helpline"},
            {"city_slug": "delhi", "service_type": "Helpline", "contact": "1091", "description": "Women's Safety Helpline - 24/7 support for women in distress"},
            
            # Mumbai services
            {"city_slug": "mumbai", "service_type": "Emergency", "contact": "112", "description": "National Emergency Number for all emergencies"},
            {"city_slug": "mumbai", "service_type": "Hospital", "contact": "108", "description": "Ambulance Service - Free emergency medical assistance"},
            {"city_slug": "mumbai", "service_type": "Police", "contact": "100", "description": "Mumbai Police Emergency Helpline"},
            {"city_slug": "mumbai", "service_type": "Helpline", "contact": "1098", "description": "Child Helpline - Support for children in need"},
            
            # Bangalore services
            {"city_slug": "bangalore", "service_type": "Emergency", "contact": "112", "description": "National Emergency Number for all emergencies"},
            {"city_slug": "bangalore", "service_type": "Hospital", "contact": "108", "description": "Ambulance Service - 24/7 emergency medical assistance"},
            {"city_slug": "bangalore", "service_type": "Police", "contact": "100", "description": "Bangalore City Police Emergency Helpline"},
            {"city_slug": "bangalore", "service_type": "Helpline", "contact": "080-22943225", "description": "Bangalore One Citizen Service Center"},
        ]
        await db.services.insert_many(services_data)
        
        logging.info("Database seeded with cities and services")


# API Routes
@api_router.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AskMyCity API is running"}


@api_router.get("/cities", response_model=List[City])
async def get_cities():
    """
    Fetch all available cities
    """
    cities = await db.cities.find({}, {"_id": 0}).to_list(100)
    return cities


@api_router.get("/cities/{city_slug}", response_model=CityWithServices)
async def get_city_services(city_slug: str):
    """
    Fetch city details and all services for a specific city
    """
    # Check if city exists
    city = await db.cities.find_one({"slug": city_slug}, {"_id": 0})
    
    if not city:
        raise HTTPException(status_code=404, detail=f"City '{city_slug}' not found")
    
    # Fetch services for the city
    services = await db.services.find({"city_slug": city_slug}, {"_id": 0}).to_list(100)
    
    return {
        "name": city["name"],
        "slug": city["slug"],
        "services": services
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_db():
    """Seed database on startup"""
    await seed_database()


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()