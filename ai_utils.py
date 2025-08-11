from transformers import pipeline

# Load sentiment-analysis pipeline once (this will download the model on first run)
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text: str) -> str:
    """
    Analyze sentiment of the input text using a Hugging Face transformers pipeline.
    Returns: 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'
    """
    if not text:
        return "NEUTRAL"

    result = sentiment_analyzer(text[:512])  # limit to 512 tokens max
    label = result[0]['label'].upper()
    # Hugging Face returns labels like 'POSITIVE' or 'NEGATIVE'
    if label not in ["POSITIVE", "NEGATIVE"]:
        return "NEUTRAL"
    return label

def generate_reply(text: str) -> str:
    """
    Generate a simple reply based on the sentiment.
    """
    sentiment = analyze_sentiment(text)
    if sentiment == "POSITIVE":
        return "Thank you for your positive feedback!"
    elif sentiment == "NEGATIVE":
        return "We’re sorry to hear about your experience. We will look into this."
    else:
        return "Thank you for reaching out. We will review your message."

