from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from database import get_db, init_db
import crud
from generate_random_users import create_random_users
from crud import clear_users_table

app = FastAPI()
origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database at the start of the application
@app.on_event("startup")
def startup_event():
    init_db()

# Mount the 'frontend' folder to serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def read_root():
    return {"message": "Hello from the FastAPI Backend!"}

# Create a new user
@app.post("/users/")
async def create_user(name: str, email: str, password: str, db=Depends(get_db)):
    try:
        user_id = crud.create_user(db, name, email, password)
        return {"id": user_id, "name": name, "email": email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()  # Close the database connection

# Get a user by email
@app.get("/users/{email}")
async def read_user(email: str, db=Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)  # Convert sqlite3.Row to dictionary for JSON response

# Get all users
@app.get("/users/")
async def read_users(db=Depends(get_db)):
    users = crud.get_users(db)
    return [dict(user) for user in users]  # Convert sqlite3.Row to dictionary

# Get all user emails
@app.get("/users/emails/")
async def read_user_emails(db=Depends(get_db)):
    emails = crud.get_all_user_emails(db)
    return [email[0] for email in emails]  # Extract the email from each tuple

