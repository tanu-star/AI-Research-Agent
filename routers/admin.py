from fastapi import APIRouter, Depends, HTTPException
from app.database import db
from routers.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_stats():
    return {
        "status": "running",
        "version": "1.0.0",
        "uptime": datetime.now().isoformat(),
        "models_loaded": {
            "summarizer": "facebook/bart-large-cnn",
            "classifier": "facebook/bart-large-mnli",
            "sentiment": "distilbert-base-uncased-finetuned-sst-2-english"
        }
    }


@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Research Assistant"}


@router.get("/users")
def get_all_users(username: str = Depends(get_current_user)):
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, created_at FROM users")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "username": r[1], "email": r[2], "created_at": r[3]} for r in rows]


@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, username: str = Depends(get_current_user)):
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "email": row[2], "created_at": row[3]}
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}")
def delete_user(user_id: int, username: str = Depends(get_current_user)):
    conn = db.get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


@router.get("/search-history")
def get_all_search_history(username: str = Depends(get_current_user)):
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM research_history ORDER BY created_at DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "user_id": r[1], "query": r[2], "results": r[3], "created_at": r[4]}
            for r in rows]
