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

load_dotenv()
password : str = os.getenv("PASSWORD")
SECRET_KEY : str = os.getenv("SECRET_KEY")

uri : str = f"mongodb+srv://samarthsam38:{password}@cluster0.vf2ar.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client: AsyncIOMotorClient = AsyncIOMotorClient(uri)

db = client['college_appointments']

@app.on_event("startup")
async def startup_event():
    """
    Actions to perform when the app starts.
    """
    try:
        await client.admin.command("ping")  # Test MongoDB connection
        print("Connected to MongoDB Atlas")
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform when the app shuts down.
    """
    client.close()
    print("MongoDB connection closed")

