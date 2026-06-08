from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Config
from app.database import db
from routers import auth, research, admin

app = FastAPI(title="AI Research Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(research.router)
app.include_router(admin.router)


@app.get("/")
def home():
    return {"message": "AI Research Assistant API", "version": "1.0.0", "status": "running"}
