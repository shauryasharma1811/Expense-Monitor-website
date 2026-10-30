from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from app.core.config import Settings
import sys
from starlette.requests import Request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# In-memory storage for token revocation (logout) and rate limiting
revoked_tokens = set()
login_attempts = {}

auth_router = APIRouter()

def get_client_ip() -> str:
    frame = sys._getframe()
    while frame:
        for val in frame.f_locals.values():
            if isinstance(val, Request):
                return val.client.host if val.client else "127.0.0.1"
            if isinstance(val, dict) and "type" in val and "client" in val:
                client = val.get("client")
                if client and len(client) > 0:
                    return client[0]
        frame = frame.f_back
    return "127.0.0.1"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Enforce rate limit (5 attempts per IP per hour)
    ip = get_client_ip()
    now = datetime.utcnow()
    window = timedelta(hours=1)

    if ip not in login_attempts:
        login_attempts[ip] = []

    # Clean up old attempts
    login_attempts[ip] = [t for t in login_attempts[ip] if now - t < window]

    if len(login_attempts[ip]) >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded: 5 login attempts per hour allowed."
        )

    login_attempts[ip].append(now)
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

import uuid
from app.core.database import SessionLocal
from app.models.models import RevokedToken

def revoke_token(token: str) -> None:
    revoked_tokens.add(token)
    db = SessionLocal()
    try:
        if not db.query(RevokedToken).filter(RevokedToken.token == token).first():
            rev = RevokedToken(id=str(uuid.uuid4()), token=token)
            db.add(rev)
            db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token in revoked_tokens:
        raise credentials_exception

    db = SessionLocal()
    try:
        is_revoked = db.query(RevokedToken).filter(RevokedToken.token == token).first()
        if is_revoked:
            revoked_tokens.add(token)
            raise credentials_exception
    except HTTPException:
        raise
    except Exception:
        pass
    finally:
        db.close()

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return {"username": username}
    except JWTError:
        raise credentials_exception

@auth_router.post("/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    revoke_token(token)
    return {"message": "Successfully logged out and token revoked."}
