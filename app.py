import uvicorn

from src import app
from src.api.signup_login import router as signup_login_router

app.include_router(signup_login_router)

@app.get("/")
async def root():
    return {"message": "Welcome to College Appointments!"}

def start():
    """
    Run the application
    """
    print("Starting the application")
    uvicorn.run(app, host="127.0.0.1", port=8000 , reload=True)

if __name__ == "__main__":
    start()