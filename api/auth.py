"""
Local JWT authentication.
ponytail: Replace verify_token() with MSAL verify when Azure creds are ready.
          All other code (main.py) stays unchanged — only this file changes.
"""
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import bcrypt

SECRET_KEY  = os.environ.get("JWT_SECRET", "change-me-local-dev-secret")
ALGORITHM   = "HS256"
TOKEN_TTL_H = int(os.environ.get("TOKEN_TTL_HOURS", "8"))

bearer_scheme = HTTPBearer(auto_error=False)

# ── Local admin accounts ──────────────────────────────────────────────────────
# Loaded from env: ADMIN_USERS=email:bcrypt_hash,email2:bcrypt_hash
# For quick setup: set plain-text ADMIN_PASSWORD + ADMIN_USERNAME
_USERS: dict[str, str] = {}  # email → hashed password

def _load_users():
    # Simple single-admin mode
    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD", "")
    if password:
        _USERS[username] = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Multi-user: ADMIN_USERS=user1@x.com:hash1,user2@x.com:hash2
    raw = os.environ.get("ADMIN_USERS", "")
    for entry in raw.split(","):
        entry = entry.strip()
        if ":" in entry:
            email, hashed = entry.split(":", 1)
            _USERS[email.strip()] = hashed.strip()

_load_users()


def authenticate(username: str, password: str) -> dict:
    hashed = _USERS.get(username)
    if not hashed or not bcrypt.checkpw(password.encode(), hashed.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"email": username, "name": username.split("@")[0]}


def create_token(user: dict) -> str:
    payload = {
        "sub": user["email"],
        "name": user.get("name", ""),
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_TTL_H),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> dict:
    """Verify local JWT. ponytail: swap body with MSAL verify for production."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return {"email": payload["sub"], "name": payload.get("name", "")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
