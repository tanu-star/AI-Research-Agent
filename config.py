import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123456789")
    JWT_SECRET = os.getenv("JWT_SECRET", "jwtsecretkey123456789")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE = 30
