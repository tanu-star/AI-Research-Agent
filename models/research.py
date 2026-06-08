from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ResearchRequest(BaseModel):
    query: str
    num_sources: int = 5

class ResearchResult(BaseModel):
    title: str
    link: str
    summary: str
    date: Optional[str] = None
    topic: Optional[str] = None
    topic_confidence: Optional[float] = None
    sentiment: Optional[str] = None
    sentiment_confidence: Optional[float] = None

class ResearchResponse(BaseModel):
    query: str
    results: List[ResearchResult]
    count: int
    timestamp: str