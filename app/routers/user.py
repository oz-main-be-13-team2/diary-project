from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    TokenResponse,
    UserLoginRequest,
    UserSignupRequest,
    UserSignupResponse,
)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/signup", response_model=UserSignupResponse, status_code=201)
def signup(payload: UserSignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        nickname=payload.nickname,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=token)
