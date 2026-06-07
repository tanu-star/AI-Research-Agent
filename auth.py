from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import db
from models.user import UserCreate
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import Config

router = APIRouter(tags=["Authentication"])
security = OAuth2PasswordBearer(tokenUrl="token")


def create_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE)
    return jwt.encode(
        {"sub": username, "exp": expire},
        Config.JWT_SECRET,
        algorithm=Config.ALGORITHM
    )


# /register - matches what main_ui.py calls
@router.post("/register")
def register(user: UserCreate):
    if db.create_user(user.username, user.email, user.password):
        return {"message": "User created successfully"}
    raise HTTPException(status_code=400, detail="Username already exists")


# /token - matches what main_ui.py calls (OAuth2 form)
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user["username"])
    return {"access_token": token, "token_type": "bearer"}


# /auth/login - alternative login endpoint
@router.post("/auth/login")
def login_alt(form_data: OAuth2PasswordRequestForm = Depends()):
    return login(form_data)


def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
