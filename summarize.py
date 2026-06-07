from transformers import pipeline
from typing import Optional

class SummarizeService:
    """Custom summarization service wrapper"""
    
    def __init__(self):
        print("Loading summarization service...")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        print("Summarization service loaded!")
    
    def summarize(self, text: str, max_length: int = 200, min_length: int = 50) -> str:
        """Summarize text"""
        if not text or len(text) < 50:
            return "Text too short to summarize"
        
        if len(text) > 1500:
            text = text[:1500]
        
        try:
            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            return result[0]["summary_text"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def summarize_batch(self, texts: list) -> list:
        """Summarize multiple texts"""
        return [self.summarize(text) for text in texts]

summarize_service = SummarizeService()