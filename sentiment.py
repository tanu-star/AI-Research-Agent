from transformers import pipeline
from typing import Dict

class SentimentAnalyzer:
    """Sentiment analysis on articles"""
    
    def __init__(self):
        print("Loading sentiment model...")
        self.analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        print("Sentiment analyzer loaded!")
    
    def analyze(self, text: str) -> Dict:
        """Analyze sentiment of text"""
        if not text or len(text) < 20:
            return {"sentiment": "NEUTRAL", "confidence": 0.0}
        
        text = text[:300]
        
        try:
            result = self.analyzer(text)[0]
            return {"sentiment": result["label"], "confidence": round(result["score"], 3)}
        except:
            return {"sentiment": "NEUTRAL", "confidence": 0.0}

sentiment_analyzer = SentimentAnalyzer()