from transformers import pipeline

# Initialize sentiment-analysis or other task pipeline once
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_email_body(text: str) -> str:
    result = sentiment_analyzer(text)
    return result[0]['label']  # e.g., 'POSITIVE', 'NEGATIVE'
