from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from trace_invest.db import SessionLocal
from trace_invest.db.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.environ.get("TRACE_SECRET", "trace-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


class RegisterPayload(BaseModel):
    username: str
    password: str


class LoginPayload(BaseModel):
    username: str
    password: str


def _get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()


def _create_user(db, username: str, password: str):
    hashed = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
    else:
        token = authorization
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        db = SessionLocal()
        user = _get_user_by_username(db, username)
        db.close()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register")
def register(p: RegisterPayload):
    db = SessionLocal()
    if _get_user_by_username(db, p.username):
        db.close()
        raise HTTPException(status_code=400, detail="user exists")
    user = _create_user(db, p.username, p.password)
    db.close()
    return {"username": user.username}


@router.post("/login")
def login(p: LoginPayload):
    db = SessionLocal()
    user = _get_user_by_username(db, p.username)
    if not user or not _verify_password(p.password, user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, detail="invalid credentials")
    access_token = _create_access_token({"sub": user.username})
    db.close()
    return {"access_token": access_token}
