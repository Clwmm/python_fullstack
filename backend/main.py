import schemas
import models
import jwt
from datetime import datetime
from models import User, Token
from database import Base, engine, SessionLocal
from utils import create_access_token,create_refresh_token,verify_password,get_hashed_password
from sqlalchemy.orm import Session
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from auth_bearer import JWTBearer
from functools import wraps



Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def check_session_and_return_user_id(token, db) -> str:
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    token_record = db.query(models.Token).filter(models.Token.user_id.is_(user_id)).first()
    if token_record is None:
        raise HTTPException(status_code=400, detail="Session not found")
    return user_id

app = FastAPI()
origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    existing_user_email = db.query(models.User).filter_by(email=user.email).first()
    existing_user_name  = db.query(models.User).filter_by(username=user.username).first()
    if existing_user_email or existing_user_name:
        raise HTTPException(status_code=400, detail="User already registered")

    encrypted_password =get_hashed_password(user.password)

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"user created successfully"}

@app.post('/login' ,response_model=schemas.TokenSchema)
def login(request: schemas.requestdetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    
    access=create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = models.Token(user=user,  access_toke=access,  refresh_toke=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }

@app.get('/getusers')
def getusers( dependencies=Depends(JWTBearer()),db: Session = Depends(get_session)):
    check_session_and_return_user_id(dependencies, db)
    user = db.query(models.User).all()
    return user

@app.get('/getuser')
def getusers( dependencies=Depends(JWTBearer()),db: Session = Depends(get_session)):
    user_id = check_session_and_return_user_id(dependencies, db)
    user = db.query(models.User).filter(models.User.id.is_(user_id)).first()
    print(type(user_id))
    return user

@app.get('/session')
def getusers( dependencies=Depends(JWTBearer()),db: Session = Depends(get_session)):
    check_session_and_return_user_id(dependencies, db)

@app.post('/change-password')
def change_password(request: schemas.changepassword, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()
    
    return {"message": "Password changed successfully"}

@app.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_session)):
    user_id = check_session_and_return_user_id(dependencies, db)
    db.query(models.Token).filter(models.Token.user_id.is_(user_id)).delete()
    db.commit()
    return {"message":"Logout Successfully"} 




