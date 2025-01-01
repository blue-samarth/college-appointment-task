import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


app : FastAPI = FastAPI()

# we will add CORS middleware to allow requests from frontend
app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load the environment variables
load_dotenv()
password = os.getenv("MONGO_PASSWORD")

client : AsyncIOMotorClient = AsyncIOMotorClient(os.getenv(f"mongodb+srv://samarthsam38:{password}@cluster0.vf2ar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"))

# try:
#     client.admin.command("ping")
#     print("Connected to MongoDB")
# except Exception as e:
#     print(f"Error in connecting to MongoDB: {e}")

db = client['college_appointments']

SECRET_KEY = os.getenv("SECRET_KEY")
