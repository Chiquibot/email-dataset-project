from transformers import pipeline

emotion_classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")

def analyze_email_body(text: str) -> str:
    result = emotion_classifier(text)
    label = result[0]['label']
    return label.upper()
