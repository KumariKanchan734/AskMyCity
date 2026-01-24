from fastapi import FastAPI, APIRouter, HTTPException, Query
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
class State(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    name: str
    slug: str

class City(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    name: str
    slug: str
    state_slug: str

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
    state_name: str
    services: List[Service]


# Comprehensive India-wide database seeding
async def seed_database():
    """
    Pre-populate the database with all Indian states, cities, and services
    """
    # Check if states already exist
    states_count = await db.states.count_documents({})
    
    if states_count == 0:
        logging.info("Seeding database with Indian states, cities, and services...")
        
        # Insert all Indian states and Union Territories
        states_data = [
            # States
            {"name": "Andhra Pradesh", "slug": "andhra-pradesh"},
            {"name": "Arunachal Pradesh", "slug": "arunachal-pradesh"},
            {"name": "Assam", "slug": "assam"},
            {"name": "Bihar", "slug": "bihar"},
            {"name": "Chhattisgarh", "slug": "chhattisgarh"},
            {"name": "Goa", "slug": "goa"},
            {"name": "Gujarat", "slug": "gujarat"},
            {"name": "Haryana", "slug": "haryana"},
            {"name": "Himachal Pradesh", "slug": "himachal-pradesh"},
            {"name": "Jharkhand", "slug": "jharkhand"},
            {"name": "Karnataka", "slug": "karnataka"},
            {"name": "Kerala", "slug": "kerala"},
            {"name": "Madhya Pradesh", "slug": "madhya-pradesh"},
            {"name": "Maharashtra", "slug": "maharashtra"},
            {"name": "Manipur", "slug": "manipur"},
            {"name": "Meghalaya", "slug": "meghalaya"},
            {"name": "Mizoram", "slug": "mizoram"},
            {"name": "Nagaland", "slug": "nagaland"},
            {"name": "Odisha", "slug": "odisha"},
            {"name": "Punjab", "slug": "punjab"},
            {"name": "Rajasthan", "slug": "rajasthan"},
            {"name": "Sikkim", "slug": "sikkim"},
            {"name": "Tamil Nadu", "slug": "tamil-nadu"},
            {"name": "Telangana", "slug": "telangana"},
            {"name": "Tripura", "slug": "tripura"},
            {"name": "Uttar Pradesh", "slug": "uttar-pradesh"},
            {"name": "Uttarakhand", "slug": "uttarakhand"},
            {"name": "West Bengal", "slug": "west-bengal"},
            # Union Territories
            {"name": "Andaman and Nicobar Islands", "slug": "andaman-nicobar"},
            {"name": "Chandigarh", "slug": "chandigarh"},
            {"name": "Dadra and Nagar Haveli and Daman and Diu", "slug": "dadra-nagar-haveli-daman-diu"},
            {"name": "Delhi", "slug": "delhi"},
            {"name": "Jammu and Kashmir", "slug": "jammu-kashmir"},
            {"name": "Ladakh", "slug": "ladakh"},
            {"name": "Lakshadweep", "slug": "lakshadweep"},
            {"name": "Puducherry", "slug": "puducherry"},
        ]
        await db.states.insert_many(states_data)
        
        # Insert major cities for each state
        cities_data = [
            # Andhra Pradesh
            {"name": "Visakhapatnam", "slug": "visakhapatnam", "state_slug": "andhra-pradesh"},
            {"name": "Vijayawada", "slug": "vijayawada", "state_slug": "andhra-pradesh"},
            {"name": "Guntur", "slug": "guntur", "state_slug": "andhra-pradesh"},
            
            # Arunachal Pradesh
            {"name": "Itanagar", "slug": "itanagar", "state_slug": "arunachal-pradesh"},
            {"name": "Naharlagun", "slug": "naharlagun", "state_slug": "arunachal-pradesh"},
            
            # Assam
            {"name": "Guwahati", "slug": "guwahati", "state_slug": "assam"},
            {"name": "Silchar", "slug": "silchar", "state_slug": "assam"},
            {"name": "Dibrugarh", "slug": "dibrugarh", "state_slug": "assam"},
            
            # Bihar
            {"name": "Patna", "slug": "patna", "state_slug": "bihar"},
            {"name": "Gaya", "slug": "gaya", "state_slug": "bihar"},
            {"name": "Bhagalpur", "slug": "bhagalpur", "state_slug": "bihar"},
            
            # Chhattisgarh
            {"name": "Raipur", "slug": "raipur", "state_slug": "chhattisgarh"},
            {"name": "Bhilai", "slug": "bhilai", "state_slug": "chhattisgarh"},
            {"name": "Bilaspur", "slug": "bilaspur-chhattisgarh", "state_slug": "chhattisgarh"},
            
            # Goa
            {"name": "Panaji", "slug": "panaji", "state_slug": "goa"},
            {"name": "Margao", "slug": "margao", "state_slug": "goa"},
            
            # Gujarat
            {"name": "Ahmedabad", "slug": "ahmedabad", "state_slug": "gujarat"},
            {"name": "Surat", "slug": "surat", "state_slug": "gujarat"},
            {"name": "Vadodara", "slug": "vadodara", "state_slug": "gujarat"},
            
            # Haryana
            {"name": "Gurugram", "slug": "gurugram", "state_slug": "haryana"},
            {"name": "Faridabad", "slug": "faridabad", "state_slug": "haryana"},
            {"name": "Panipat", "slug": "panipat", "state_slug": "haryana"},
            
            # Himachal Pradesh
            {"name": "Shimla", "slug": "shimla", "state_slug": "himachal-pradesh"},
            {"name": "Manali", "slug": "manali", "state_slug": "himachal-pradesh"},
            {"name": "Dharamshala", "slug": "dharamshala", "state_slug": "himachal-pradesh"},
            
            # Jharkhand
            {"name": "Ranchi", "slug": "ranchi", "state_slug": "jharkhand"},
            {"name": "Jamshedpur", "slug": "jamshedpur", "state_slug": "jharkhand"},
            {"name": "Dhanbad", "slug": "dhanbad", "state_slug": "jharkhand"},
            
            # Karnataka
            {"name": "Bangalore", "slug": "bangalore", "state_slug": "karnataka"},
            {"name": "Mysore", "slug": "mysore", "state_slug": "karnataka"},
            {"name": "Mangalore", "slug": "mangalore", "state_slug": "karnataka"},
            
            # Kerala
            {"name": "Kochi", "slug": "kochi", "state_slug": "kerala"},
            {"name": "Thiruvananthapuram", "slug": "thiruvananthapuram", "state_slug": "kerala"},
            {"name": "Kozhikode", "slug": "kozhikode", "state_slug": "kerala"},
            
            # Madhya Pradesh
            {"name": "Bhopal", "slug": "bhopal", "state_slug": "madhya-pradesh"},
            {"name": "Indore", "slug": "indore", "state_slug": "madhya-pradesh"},
            {"name": "Gwalior", "slug": "gwalior", "state_slug": "madhya-pradesh"},
            
            # Maharashtra
            {"name": "Mumbai", "slug": "mumbai", "state_slug": "maharashtra"},
            {"name": "Pune", "slug": "pune", "state_slug": "maharashtra"},
            {"name": "Nagpur", "slug": "nagpur", "state_slug": "maharashtra"},
            
            # Manipur
            {"name": "Imphal", "slug": "imphal", "state_slug": "manipur"},
            {"name": "Churachandpur", "slug": "churachandpur", "state_slug": "manipur"},
            
            # Meghalaya
            {"name": "Shillong", "slug": "shillong", "state_slug": "meghalaya"},
            {"name": "Tura", "slug": "tura", "state_slug": "meghalaya"},
            
            # Mizoram
            {"name": "Aizawl", "slug": "aizawl", "state_slug": "mizoram"},
            {"name": "Lunglei", "slug": "lunglei", "state_slug": "mizoram"},
            
            # Nagaland
            {"name": "Kohima", "slug": "kohima", "state_slug": "nagaland"},
            {"name": "Dimapur", "slug": "dimapur", "state_slug": "nagaland"},
            
            # Odisha
            {"name": "Bhubaneswar", "slug": "bhubaneswar", "state_slug": "odisha"},
            {"name": "Cuttack", "slug": "cuttack", "state_slug": "odisha"},
            {"name": "Rourkela", "slug": "rourkela", "state_slug": "odisha"},
            
            # Punjab
            {"name": "Chandigarh", "slug": "chandigarh-punjab", "state_slug": "punjab"},
            {"name": "Ludhiana", "slug": "ludhiana", "state_slug": "punjab"},
            {"name": "Amritsar", "slug": "amritsar", "state_slug": "punjab"},
            
            # Rajasthan
            {"name": "Jaipur", "slug": "jaipur", "state_slug": "rajasthan"},
            {"name": "Jodhpur", "slug": "jodhpur", "state_slug": "rajasthan"},
            {"name": "Udaipur", "slug": "udaipur", "state_slug": "rajasthan"},
            
            # Sikkim
            {"name": "Gangtok", "slug": "gangtok", "state_slug": "sikkim"},
            {"name": "Namchi", "slug": "namchi", "state_slug": "sikkim"},
            
            # Tamil Nadu
            {"name": "Chennai", "slug": "chennai", "state_slug": "tamil-nadu"},
            {"name": "Coimbatore", "slug": "coimbatore", "state_slug": "tamil-nadu"},
            {"name": "Madurai", "slug": "madurai", "state_slug": "tamil-nadu"},
            
            # Telangana
            {"name": "Hyderabad", "slug": "hyderabad", "state_slug": "telangana"},
            {"name": "Warangal", "slug": "warangal", "state_slug": "telangana"},
            {"name": "Nizamabad", "slug": "nizamabad", "state_slug": "telangana"},
            
            # Tripura
            {"name": "Agartala", "slug": "agartala", "state_slug": "tripura"},
            {"name": "Udaipur", "slug": "udaipur-tripura", "state_slug": "tripura"},
            
            # Uttar Pradesh
            {"name": "Lucknow", "slug": "lucknow", "state_slug": "uttar-pradesh"},
            {"name": "Kanpur", "slug": "kanpur", "state_slug": "uttar-pradesh"},
            {"name": "Agra", "slug": "agra", "state_slug": "uttar-pradesh"},
            
            # Uttarakhand
            {"name": "Dehradun", "slug": "dehradun", "state_slug": "uttarakhand"},
            {"name": "Haridwar", "slug": "haridwar", "state_slug": "uttarakhand"},
            {"name": "Nainital", "slug": "nainital", "state_slug": "uttarakhand"},
            
            # West Bengal
            {"name": "Kolkata", "slug": "kolkata", "state_slug": "west-bengal"},
            {"name": "Howrah", "slug": "howrah", "state_slug": "west-bengal"},
            {"name": "Durgapur", "slug": "durgapur", "state_slug": "west-bengal"},
            
            # Union Territories
            {"name": "Port Blair", "slug": "port-blair", "state_slug": "andaman-nicobar"},
            {"name": "Chandigarh City", "slug": "chandigarh-city", "state_slug": "chandigarh"},
            {"name": "Daman", "slug": "daman", "state_slug": "dadra-nagar-haveli-daman-diu"},
            {"name": "New Delhi", "slug": "new-delhi", "state_slug": "delhi"},
            {"name": "Srinagar", "slug": "srinagar", "state_slug": "jammu-kashmir"},
            {"name": "Jammu", "slug": "jammu", "state_slug": "jammu-kashmir"},
            {"name": "Leh", "slug": "leh", "state_slug": "ladakh"},
            {"name": "Kavaratti", "slug": "kavaratti", "state_slug": "lakshadweep"},
            {"name": "Puducherry City", "slug": "puducherry-city", "state_slug": "puducherry"},
        ]
        await db.cities.insert_many(cities_data)
        
        # Create services template (12 types) - will be applied to each city
        services_template = [
            {"service_type": "Emergency", "contact": "112", "description": "National Emergency Number - All emergencies (Police, Fire, Medical)"},
            {"service_type": "Police", "contact": "100", "description": "Police Emergency Helpline - For law enforcement assistance"},
            {"service_type": "Hospital", "contact": "104", "description": "National Health Helpline - Medical consultation and ambulance"},
            {"service_type": "Ambulance", "contact": "108", "description": "Free Ambulance Service - Emergency medical transport"},
            {"service_type": "Fire Station", "contact": "101", "description": "Fire Emergency Services - Fire incidents and rescue operations"},
            {"service_type": "Women Helpline", "contact": "1091", "description": "Women's Safety Helpline - 24/7 support for women in distress"},
            {"service_type": "Child Helpline", "contact": "1098", "description": "Child Helpline - Support for children in need of care and protection"},
            {"service_type": "Tourist Helpline", "contact": "1363", "description": "India Tourism Helpline - Assistance for tourists"},
            {"service_type": "Municipal Office", "contact": "1800-XXX-XXXX", "description": "City Municipal Corporation - Civic services and complaints"},
            {"service_type": "Electricity Emergency", "contact": "1912", "description": "Power Outage Helpline - Electricity supply issues"},
            {"service_type": "Water Supply", "contact": "1916", "description": "Water Supply Helpline - Water supply issues and complaints"},
            {"service_type": "Disaster Management", "contact": "1070", "description": "Disaster Management Authority - Natural disasters and emergencies"},
        ]
        
        # Insert services for all cities
        services_data = []
        for city in cities_data:
            for service in services_template:
                services_data.append({
                    "city_slug": city["slug"],
                    "service_type": service["service_type"],
                    "contact": service["contact"],
                    "description": service["description"]
                })
        
        await db.services.insert_many(services_data)
        
        logging.info(f"Database seeded successfully: {len(states_data)} states, {len(cities_data)} cities, {len(services_data)} services")


# API Routes
@api_router.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AskMyCity API is running - India-wide coverage"}


@api_router.get("/states", response_model=List[State])
async def get_states():
    """
    Fetch all available states and union territories
    """
    states = await db.states.find({}, {"_id": 0}).sort("name", 1).to_list(100)
    return states


@api_router.get("/cities", response_model=List[City])
async def get_cities(state: Optional[str] = Query(None, description="Filter cities by state slug")):
    """
    Fetch cities, optionally filtered by state
    """
    query = {}
    if state:
        query["state_slug"] = state
    
    cities = await db.cities.find(query, {"_id": 0}).sort("name", 1).to_list(500)
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
    
    # Get state name
    state = await db.states.find_one({"slug": city["state_slug"]}, {"_id": 0})
    state_name = state["name"] if state else "Unknown"
    
    # Fetch services for the city
    services = await db.services.find({"city_slug": city_slug}, {"_id": 0}).to_list(100)
    
    return {
        "name": city["name"],
        "slug": city["slug"],
        "state_name": state_name,
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