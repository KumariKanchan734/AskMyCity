from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import aiosqlite
import os
import logging
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, AsyncGenerator
from contextlib import asynccontextmanager

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# SQLite Database Name
DB_NAME = os.environ.get('DB_NAME', 'askmycity.db')

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup: Initialize DB and seed
    await init_database()
    await seed_database()
    yield
    # Shutdown: Nothing specific for SQLite per-se as connection is per-request/managed

# Create the main app with lifespan
app = FastAPI(lifespan=lifespan)

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


async def init_database():
    """Create tables if they don't exist"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS states (
                slug TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                slug TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                state_slug TEXT NOT NULL,
                FOREIGN KEY (state_slug) REFERENCES states (slug)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_slug TEXT NOT NULL,
                service_type TEXT NOT NULL,
                contact TEXT NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (city_slug) REFERENCES cities (slug)
            )
        """)
        await db.commit()
        logging.info("Database initialized (tables verified).")


# Comprehensive India-wide database seeding
async def seed_database():
    """
    Pre-populate the database with all Indian states, cities, and services
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM states")
            row = await cursor.fetchone()
            states_count = row[0]
            
            if states_count == 0:
                logging.info("Seeding database with Indian states, cities, and services...")
            
                # Insert all Indian states and Union Territories
                states_data = [
                    # States
                    ("Andhra Pradesh", "andhra-pradesh"),
                    ("Arunachal Pradesh", "arunachal-pradesh"),
                    ("Assam", "assam"),
                    ("Bihar", "bihar"),
                    ("Chhattisgarh", "chhattisgarh"),
                    ("Goa", "goa"),
                    ("Gujarat", "gujarat"),
                    ("Haryana", "haryana"),
                    ("Himachal Pradesh", "himachal-pradesh"),
                    ("Jharkhand", "jharkhand"),
                    ("Karnataka", "karnataka"),
                    ("Kerala", "kerala"),
                    ("Madhya Pradesh", "madhya-pradesh"),
                    ("Maharashtra", "maharashtra"),
                    ("Manipur", "manipur"),
                    ("Meghalaya", "meghalaya"),
                    ("Mizoram", "mizoram"),
                    ("Nagaland", "nagaland"),
                    ("Odisha", "odisha"),
                    ("Punjab", "punjab"),
                    ("Rajasthan", "rajasthan"),
                    ("Sikkim", "sikkim"),
                    ("Tamil Nadu", "tamil-nadu"),
                    ("Telangana", "telangana"),
                    ("Tripura", "tripura"),
                    ("Uttar Pradesh", "uttar-pradesh"),
                    ("Uttarakhand", "uttarakhand"),
                    ("West Bengal", "west-bengal"),
                    # Union Territories
                    ("Andaman and Nicobar Islands", "andaman-nicobar"),
                    ("Chandigarh", "chandigarh"),
                    ("Dadra and Nagar Haveli and Daman and Diu", "dadra-nagar-haveli-daman-diu"),
                    ("Delhi", "delhi"),
                    ("Jammu and Kashmir", "jammu-kashmir"),
                    ("Ladakh", "ladakh"),
                    ("Lakshadweep", "lakshadweep"),
                    ("Puducherry", "puducherry"),
                ]
                await db.executemany("INSERT INTO states (name, slug) VALUES (?, ?)", states_data)
                
                # Insert major cities for each state
                cities_data = [
                    # Andhra Pradesh
                    ("Visakhapatnam", "visakhapatnam", "andhra-pradesh"),
                    ("Vijayawada", "vijayawada", "andhra-pradesh"),
                    ("Guntur", "guntur", "andhra-pradesh"),
                    
                    # Arunachal Pradesh
                    ("Itanagar", "itanagar", "arunachal-pradesh"),
                    ("Naharlagun", "naharlagun", "arunachal-pradesh"),
                    
                    # Assam
                    ("Guwahati", "guwahati", "assam"),
                    ("Silchar", "silchar", "assam"),
                    ("Dibrugarh", "dibrugarh", "assam"),
                    
                    # Bihar
                    ("Patna", "patna", "bihar"),
                    ("Gaya", "gaya", "bihar"),
                    ("Bhagalpur", "bhagalpur", "bihar"),
                    
                    # Chhattisgarh
                    ("Raipur", "raipur", "chhattisgarh"),
                    ("Bhilai", "bhilai", "chhattisgarh"),
                    ("Bilaspur", "bilaspur-chhattisgarh", "chhattisgarh"),
                    
                    # Goa
                    ("Panaji", "panaji", "goa"),
                    ("Margao", "margao", "goa"),
                    
                    # Gujarat
                    ("Ahmedabad", "ahmedabad", "gujarat"),
                    ("Surat", "surat", "gujarat"),
                    ("Vadodara", "vadodara", "gujarat"),
                    
                    # Haryana
                    ("Gurugram", "gurugram", "haryana"),
                    ("Faridabad", "faridabad", "haryana"),
                    ("Panipat", "panipat", "haryana"),
                    
                    # Himachal Pradesh
                    ("Shimla", "shimla", "himachal-pradesh"),
                    ("Manali", "manali", "himachal-pradesh"),
                    ("Dharamshala", "dharamshala", "himachal-pradesh"),
                    
                    # Jharkhand
                    ("Ranchi", "ranchi", "jharkhand"),
                    ("Jamshedpur", "jamshedpur", "jharkhand"),
                    ("Dhanbad", "dhanbad", "jharkhand"),
                    
                    # Karnataka
                    ("Bangalore", "bangalore", "karnataka"),
                    ("Mysore", "mysore", "karnataka"),
                    ("Mangalore", "mangalore", "karnataka"),
                    
                    # Kerala
                    ("Kochi", "kochi", "kerala"),
                    ("Thiruvananthapuram", "thiruvananthapuram", "kerala"),
                    ("Kozhikode", "kozhikode", "kerala"),
                    
                    # Madhya Pradesh
                    ("Bhopal", "bhopal", "madhya-pradesh"),
                    ("Indore", "indore", "madhya-pradesh"),
                    ("Gwalior", "gwalior", "madhya-pradesh"),
                    
                    # Maharashtra
                    ("Mumbai", "mumbai", "maharashtra"),
                    ("Pune", "pune", "maharashtra"),
                    ("Nagpur", "nagpur", "maharashtra"),
                    
                    # Manipur
                    ("Imphal", "imphal", "manipur"),
                    ("Churachandpur", "churachandpur", "manipur"),
                    
                    # Meghalaya
                    ("Shillong", "shillong", "meghalaya"),
                    ("Tura", "tura", "meghalaya"),
                    
                    # Mizoram
                    ("Aizawl", "aizawl", "mizoram"),
                    ("Lunglei", "lunglei", "mizoram"),
                    
                    # Nagaland
                    ("Kohima", "kohima", "nagaland"),
                    ("Dimapur", "dimapur", "nagaland"),
                    
                    # Odisha
                    ("Bhubaneswar", "bhubaneswar", "odisha"),
                    ("Cuttack", "cuttack", "odisha"),
                    ("Rourkela", "rourkela", "odisha"),
                    
                    # Punjab
                    ("Chandigarh", "chandigarh-punjab", "punjab"),
                    ("Ludhiana", "ludhiana", "punjab"),
                    ("Amritsar", "amritsar", "punjab"),
                    
                    # Rajasthan
                    ("Jaipur", "jaipur", "rajasthan"),
                    ("Jodhpur", "jodhpur", "rajasthan"),
                    ("Udaipur", "udaipur", "rajasthan"),
                    
                    # Sikkim
                    ("Gangtok", "gangtok", "sikkim"),
                    ("Namchi", "namchi", "sikkim"),
                    
                    # Tamil Nadu
                    ("Chennai", "chennai", "tamil-nadu"),
                    ("Coimbatore", "coimbatore", "tamil-nadu"),
                    ("Madurai", "madurai", "tamil-nadu"),
                    
                    # Telangana
                    ("Hyderabad", "hyderabad", "telangana"),
                    ("Warangal", "warangal", "telangana"),
                    ("Nizamabad", "nizamabad", "telangana"),
                    
                    # Tripura
                    ("Agartala", "agartala", "tripura"),
                    ("Udaipur", "udaipur-tripura", "tripura"),
                    
                    # Uttar Pradesh
                    ("Lucknow", "lucknow", "uttar-pradesh"),
                    ("Kanpur", "kanpur", "uttar-pradesh"),
                    ("Agra", "agra", "uttar-pradesh"),
                    
                    # Uttarakhand
                    ("Dehradun", "dehradun", "uttarakhand"),
                    ("Haridwar", "haridwar", "uttarakhand"),
                    ("Nainital", "nainital", "uttarakhand"),
                    
                    # West Bengal
                    ("Kolkata", "kolkata", "west-bengal"),
                    ("Howrah", "howrah", "west-bengal"),
                    ("Durgapur", "durgapur", "west-bengal"),
                    
                    # Union Territories
                    ("Port Blair", "port-blair", "andaman-nicobar"),
                    ("Chandigarh City", "chandigarh-city", "chandigarh"),
                    ("Daman", "daman", "dadra-nagar-haveli-daman-diu"),
                    ("New Delhi", "new-delhi", "delhi"),
                    ("Srinagar", "srinagar", "jammu-kashmir"),
                    ("Jammu", "jammu", "jammu-kashmir"),
                    ("Leh", "leh", "ladakh"),
                    ("Kavaratti", "kavaratti", "lakshadweep"),
                    ("Puducherry City", "puducherry-city", "puducherry"),
                ]
                await db.executemany("INSERT INTO cities (name, slug, state_slug) VALUES (?, ?, ?)", cities_data)
                
                # Create services template (12 types)
                services_template = [
                    ("Emergency", "112", "National Emergency Number - All emergencies (Police, Fire, Medical)"),
                    ("Police", "100", "Police Emergency Helpline - For law enforcement assistance"),
                    ("Hospital", "104", "National Health Helpline - Medical consultation and ambulance"),
                    ("Ambulance", "108", "Free Ambulance Service - Emergency medical transport"),
                    ("Fire Station", "101", "Fire Emergency Services - Fire incidents and rescue operations"),
                    ("Women Helpline", "1091", "Women's Safety Helpline - 24/7 support for women in distress"),
                    ("Child Helpline", "1098", "Child Helpline - Support for children in need of care and protection"),
                    ("Tourist Helpline", "1363", "India Tourism Helpline - Assistance for tourists"),
                    ("Municipal Office", "1800-XXX-XXXX", "City Municipal Corporation - Civic services and complaints"),
                    ("Electricity Emergency", "1912", "Power Outage Helpline - Electricity supply issues"),
                    ("Water Supply", "1916", "Water Supply Helpline - Water supply issues and complaints"),
                    ("Disaster Management", "1070", "Disaster Management Authority - Natural disasters and emergencies"),
                ]
                
                # Prepare services data for bulk insert
                services_db_data = []
                for city_name, city_slug, state_slug in cities_data:
                    for s_type, s_contact, s_desc in services_template:
                        services_db_data.append((city_slug, s_type, s_contact, s_desc))
                
                await db.executemany("""
                    INSERT INTO services (city_slug, service_type, contact, description) 
                    VALUES (?, ?, ?, ?)
                """, services_db_data)
                
                await db.commit()
                logging.info(f"Database seeded successfully: {len(states_data)} states, {len(cities_data)} cities, {len(services_db_data)} services")

    except Exception as e:
        logging.error(f"Could not seed database: {str(e)}")


# API Routes
@api_router.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AskMyCity API is running on SQLite - Offline Mode"}


@api_router.get("/states", response_model=List[State])
async def get_states():
    """
    Fetch all available states and union territories
    """
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT name, slug FROM states ORDER BY name ASC") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


@api_router.get("/cities", response_model=List[City])
async def get_cities(state: Optional[str] = Query(None, description="Filter cities by state slug")):
    """
    Fetch cities, optionally filtered by state
    """
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        query = "SELECT name, slug, state_slug FROM cities"
        params = []
        
        if state:
            query += " WHERE state_slug = ?"
            params.append(state)
            
        query += " ORDER BY name ASC"
        
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


@api_router.get("/cities/{city_slug}", response_model=CityWithServices)
async def get_city_services(city_slug: str):
    """
    Fetch city details and all services for a specific city
    """
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        
        # Check if city exists
        async with db.execute("SELECT name, slug, state_slug FROM cities WHERE slug = ?", (city_slug,)) as cursor:
            city = await cursor.fetchone()
            
        if not city:
            raise HTTPException(status_code=404, detail=f"City '{city_slug}' not found")
        
        # Get state name
        async with db.execute("SELECT name FROM states WHERE slug = ?", (city['state_slug'],)) as cursor:
            state = await cursor.fetchone()
            state_name = state['name'] if state else "Unknown"
        
        # Fetch services for the city
        async with db.execute("SELECT city_slug, service_type, contact, description FROM services WHERE city_slug = ?", (city_slug,)) as cursor:
            services = await cursor.fetchall()
            
        return {
            "name": city['name'],
            "slug": city['slug'],
            "state_name": state_name,
            "services": [dict(s) for s in services]
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