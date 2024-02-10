from better_profanity import profanity


def analyze_and_flag_negative_sentiment(dirty_text):
    """Analyze text sentiment and flag if very negative."""
    return profanity.contains_profanity(dirty_text)
