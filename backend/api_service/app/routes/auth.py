from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import User
from app.auth import hash_password, verify_password, create_access_token, get_db

router = APIRouter()

class AuthInput(BaseModel):
    username: str
    password: str

class RegisterInput(AuthInput):
    email: str

@router.post("/register")
def register(data: RegisterInput, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    hashed = hash_password(data.password)
    user = User(username=data.username, email=data.email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(data: AuthInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
