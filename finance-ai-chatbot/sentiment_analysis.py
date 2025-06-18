from textblob import TextBlob


def analyze_sentiment(text: str) -> str:
    """
    Analyzes the sentiment of a given text.
    Returns 'positive', 'neutral', or 'negative' based on sentiment polarity.
    """
    sentiment_score = TextBlob(text).sentiment.polarity

    if sentiment_score < -0.2:
        return "negative"
    elif sentiment_score > 0.2:
        return "positive"
    return "neutral"
