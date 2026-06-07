from pydantic import BaseModel
from typing import Optional, List

class SummaryRequest(BaseModel):
    text: str
    max_length: int = 200
    min_length: int = 50

class ClassificationRequest(BaseModel):
    text: str
    top_k: int = 1

class SentimentRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    model: str = "facebook/bart-large-cnn"

class ClassificationResponse(BaseModel):
    topic: str
    confidence: float
    all_topics: Optional[List[dict]] = None  # Fixed: ]] to ]

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float