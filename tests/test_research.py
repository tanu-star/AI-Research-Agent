# Test file for Research Assistant
import os
import sys


# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import services
from services.search_service import search_service
from services.extract_service import extract_service
from ml.summarizer import summarizer
from ml.classifier import classifier
from ml.sentiment import sentiment_analyzer

# ==================== Test Functions ====================

def test_search_service():
    """Test search service"""
    print("Testing search service...")
    results = search_service.search("python", 3)
    assert isinstance(results, list)
    assert len(results) > 0
    print("✓ Search test passed")

def test_extract_service():
    """Test extract service"""
    print("Testing extract service...")
    content = extract_service.extract("https://example.com")
    assert isinstance(content, dict)
    assert "title" in content
    print("✓ Extract test passed")

def test_summarizer():
    """Test summarizer"""
    print("Testing summarizer...")
    text = "Python is a high-level, general-purpose programming language created by Guido van Rossum. It emphasizes code readability."
    summary = summarizer.summarize(text)
    assert isinstance(summary, str)
    assert len(summary) > 0
    print("✓ Summarizer test passed")

def test_classifier():
    """Test classifier"""
    print("Testing classifier...")
    text = "Technology news about AI"
    topic = classifier.classify(text)
    assert isinstance(topic, dict)
    assert "topic" in topic
    print("✓ Classifier test passed")

def test_sentiment():
    """Test sentiment"""
    print("Testing sentiment...")
    sentiment = sentiment_analyzer.analyze("Great product!")
    assert isinstance(sentiment, dict)
    assert "sentiment" in sentiment
    print("✓ Sentiment test passed")

# ==================== Run All Tests ====================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Running Tests...")
    print("="*50 + "\n")
    
    try:
        test_search_service()
        test_extract_service()
        test_summarizer()
        test_classifier()
        test_sentiment()
        
        print("\n" + "="*50)
        print("All Tests Passed! ✓")
        print("="*50)
    except Exception as e:
        print(f"\nError: {e}")