from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from pathlib import Path
import json, os, hmac, hashlib, time, base64

router = APIRouter(prefix="/auth", tags=["auth"])

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
USERS_DIR = DATA_DIR / "users"
USERS_DIR.mkdir(parents=True, exist_ok=True)
USERS_FILE = USERS_DIR / "users.json"

SECRET_KEY = os.environ.get("TRACE_SECRET", "trace-secret")
TOKEN_EXP = 60 * 60 * 24 * 7


class RegisterPayload(BaseModel):
    username: str
    password: str


class LoginPayload(BaseModel):
    username: str
    password: str


def _load_users():
    if not USERS_FILE.exists():
        return {}
    try:
        return json.loads(USERS_FILE.read_text())
    except Exception:
        return {}


def _save_users(u):
    USERS_FILE.write_text(json.dumps(u, indent=2))


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _make_token(username: str) -> str:
    payload = f"{username}|{int(time.time())}"
    sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    token = base64.urlsafe_b64encode(f"{payload}|{sig}".encode()).decode()
    return token


def _verify_token(token: str):
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        parts = raw.split("|")
        if len(parts) != 3:
            return None
        username, ts, sig = parts
        payload = f"{username}|{ts}"
        expect = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expect, sig):
            return None
        if int(ts) + TOKEN_EXP < int(time.time()):
            return None
        return username
    except Exception:
        return None


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
    else:
        token = authorization
    user = _verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


@router.post("/register")
def register(p: RegisterPayload):
    users = _load_users()
    if p.username in users:
        raise HTTPException(status_code=400, detail="user exists")
    users[p.username] = {"password": _hash_password(p.password), "created_at": int(time.time())}
    _save_users(users)
    return {"username": p.username}


@router.post("/login")
def login(p: LoginPayload):
    users = _load_users()
    u = users.get(p.username)
    if not u or u.get("password") != _hash_password(p.password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = _make_token(p.username)
    return {"access_token": token}
