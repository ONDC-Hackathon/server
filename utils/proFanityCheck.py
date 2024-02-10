from google.cloud import language_v1
from google.cloud.language_v1 import types

def analyze_and_flag_negative_sentiment(text):
    """Analyze text sentiment and flag if very negative."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=types.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    if sentiment.score <= -0.75:  # Very negative sentiment
        return True
    return False
