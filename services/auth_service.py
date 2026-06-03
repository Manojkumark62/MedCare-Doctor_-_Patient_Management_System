from sqlalchemy import or_
from sqlalchemy.orm import Session
from models.users import User
from schemas.user import UserRegister
from utils.hashing import hash_password, verify_password
from utils.security import create_access_token

def register_user(data: UserRegister, db: Session):

    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        return None

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role.lower()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(identifier: str, password: str, db: Session):
    user = db.query(User).filter(
        or_(User.email == identifier, User.username == identifier)
    ).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    token = create_access_token(
        {"user_id": user.id, "role": user.role})
    return token