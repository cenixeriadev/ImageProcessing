from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserResponse , AuthInput, RegisterInput
from app.auth import hash_password, verify_password, create_access_token, get_db , get_current_user
from fastapi.responses import JSONResponse
import datetime

router = APIRouter()

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
    
    cookie_expiry = 86400 * 30 if data.remember_me else 3600
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    user.last_login = datetime.datetime.utcnow()
    db.commit()  # Commit the changes to update last_login
    db.refresh(user)
    
    token = create_access_token({"sub": user.username})
    response = JSONResponse(content={"access_token": token, "token_type": "bearer"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="strict",
        secure=False,  # cambia a True en producción con HTTPS
        max_age= 3000
    )
    return response
@router.post("/logout")
def logout():
    response = JSONResponse(content={"message": "logged out"})
    response.delete_cookie("access_token")
    return response

@router.get("/me", response_model= UserResponse)
def me(user: User = Depends(get_current_user)):
    return user

