from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from schemas.user import UserRegister, UserRegisterResponse, TokenResponse
from services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRegisterResponse, status_code=201)
def register(user: UserRegister, db: Session = Depends(get_db)):
    result = register_user(user, db)

    if not result:
        raise HTTPException(status_code=400, detail="Email already exists")

    return {"info": "User registered successfully", "user": result}

@router.post("/login", response_model=TokenResponse)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = login_user(data.username, data.password, db)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"}
