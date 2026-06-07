from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

class Summarizer:
    """Article summarization using BART model"""
    
    def __init__(self):
        print("Loading BART summarization model...")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        print("Model loaded!")
    
    def summarize(self, text: str, max_length: int = 200, min_length: int = 50) -> str:
        """Generate summary from text"""
        if not text or len(text) < 50:
            return "Text too short"
        
        if len(text) > 1024:
            text = text[:1024]
        
        try:
            inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = self.model.generate(
                inputs["input_ids"],
                num_beams=4,
                max_length=max_length,
                min_length=min_length,
                length_penalty=2.0,
                early_stopping=True
            )
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
        except Exception as e:
            return text[:300] + "..."

# Initialize global summarizer
summarizer = Summarizer()