from fastapi import APIRouter, Depends
from routers.auth import get_current_user
from services.search_service import search_service
from services.extract_service import extract_service
from ml.summarizer import summarizer
from ml.classifier import classifier
from ml.sentiment import sentiment_analyzer
from app.database import db
from models.research import ResearchRequest, ResearchResponse, ResearchResult
from datetime import datetime

router = APIRouter(prefix="/research", tags=["Research"])


@router.post("/", response_model=ResearchResponse)
def research(request: ResearchRequest, username: str = Depends(get_current_user)):
    search_results = search_service.search(request.query, request.num_sources)
    
    results = []
    for r in search_results:
        if "error" in r:
            continue
        content = extract_service.extract(r["link"])
        
        if content.get("text") and len(content["text"]) > 50:
            summary = summarizer.summarize(content["text"])
            topic = classifier.classify(content["text"])
            sentiment = sentiment_analyzer.analyze(summary)
            
            results.append(ResearchResult(
                title=content.get("title") or r.get("title", "Untitled"),
                link=r["link"],
                summary=summary,
                date=content.get("date"),
                topic=topic.get("topic"),
                topic_confidence=topic.get("confidence"),
                sentiment=sentiment.get("sentiment"),
                sentiment_confidence=sentiment.get("confidence")
            ))
    
    # Save to history
    user = db.get_user_by_username(username)
    if user:
        db.save_research(user["id"], request.query,
                         [r.dict() for r in results])
    
    return ResearchResponse(
        query=request.query,
        results=results,
        count=len(results),
        timestamp=datetime.now().isoformat()
    )


@router.get("/history")
def get_history(username: str = Depends(get_current_user), limit: int = 10):
    user = db.get_user_by_username(username)
    
    if user:
        return db.get_history(user["id"], limit)
    return []
