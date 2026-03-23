import random

# Use NLTK VADER for quick sentiment analysis when available.
# Fall back to a lightweight keyword-based sentiment heuristic when it's not installed,
# so the site still works and users don't hit a 500 on submit.
try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    import nltk
    _HAS_NLTK = True
except Exception:
    SentimentIntensityAnalyzer = None
    _HAS_NLTK = False


def _ensure_vader():
    """Ensure VADER is available.

    This function attempts to import NLTK and (if present) download and initialize
    the VADER SentimentIntensityAnalyzer. It re-attempts imports at runtime so
    installing NLTK while the server is running will be picked up without a
    restart.
    """
    global SentimentIntensityAnalyzer, _HAS_NLTK
    try:
        import nltk
        # NLTK is importable now
        _HAS_NLTK = True
        if SentimentIntensityAnalyzer is None:
            try:
                # quiet=True avoids interactive output when downloading
                nltk.download('vader_lexicon', quiet=True)
                from nltk.sentiment import SentimentIntensityAnalyzer as SIA  # type: ignore
                SentimentIntensityAnalyzer = SIA
                print("[freedom] NLTK VADER loaded successfully.")
            except Exception:
                # If initialization fails, fall back but keep NLTK marked unavailable
                SentimentIntensityAnalyzer = None
                _HAS_NLTK = False
    except Exception:
        # NLTK still not available; stay in fallback mode
        _HAS_NLTK = False
        SentimentIntensityAnalyzer = None


def _fallback_sentiment(text: str) -> float:
    """Very small heuristic sentiment scorer in [-1.0, 1.0].
    This is a fallback when NLTK isn't installed; it uses small positive/negative
    word lists and returns a coarse polarity estimate.
    """
    positives = {"happy", "joy", "love", "relieved", "good", "grateful", "calm", "peace"}
    negatives = {"sad", "angry", "hate", "miserable", "depressed", "alone", "anxious", "worried", "panic"}
    score = 0.0
    words = ["".join(ch for ch in w if ch.isalpha()) for w in text.lower().split()]
    for w in words:
        if w in positives:
            score += 0.5
        if w in negatives:
            score -= 0.5
    # normalize by number of words to avoid huge scores
    if words:
        score = score / max(1, len(words) / 5)
    # clamp
    return max(-1.0, min(1.0, score))


SONG_LIBRARY = {
    'very_sad': [
        {'title': 'Fix You', 'artist': 'Coldplay', 'url': 'https://www.youtube.com/watch?v=k4V3Mo61fJM'},
        {'title': 'Let Her Go', 'artist': 'Passenger', 'url': 'https://www.youtube.com/watch?v=RBumgq5yVrA'},
    ],
    'sad': [
        {'title': 'Skinny Love', 'artist': 'Bon Iver', 'url': 'https://www.youtube.com/watch?v=ssdgFoHLwnk'},
        {'title': 'The Night We Met', 'artist': 'Lord Huron', 'url': 'https://www.youtube.com/watch?v=KtlgYxa6BMU'},
    ],
    'anxious': [
        {'title': 'Holocene', 'artist': 'Bon Iver', 'url': 'https://www.youtube.com/watch?v=TWcyIpul8OE'},
        {'title': 'Breathe Me', 'artist': 'Sia', 'url': 'https://www.youtube.com/watch?v=ghPcYqn0p4Y'},
    ],
    'angry': [
        {'title': 'Let It Be', 'artist': 'The Beatles', 'url': 'https://www.youtube.com/watch?v=QDYfEBY9NM4'},
        {'title': 'I Won\'t Back Down', 'artist': 'Tom Petty', 'url': 'https://www.youtube.com/watch?v=wL5f-3fXJng'},
    ],
    'neutral': [
        {'title': 'Weightless', 'artist': 'Marconi Union', 'url': 'https://www.youtube.com/watch?v=UfcAVejslrU'},
        {'title': 'River Flows In You', 'artist': 'Yiruma', 'url': 'https://www.youtube.com/watch?v=7maJOI3QMu0'},
    ],
    'uplifted': [
        {'title': 'Here Comes The Sun', 'artist': 'The Beatles', 'url': 'https://www.youtube.com/watch?v=KQetemT1sWc'},
        {'title': 'Better Together', 'artist': 'Jack Johnson', 'url': 'https://www.youtube.com/watch?v=u57d4_b_YgI'},
    ],
}


# Map canonical emotions to colors (hex)
EMOTION_COLOR_MAP = {
    'angry': '#ff6b6b',       # warm red
    'sad': '#6b8cff',         # soft blue
    'happy': '#ffd166',       # warm yellow
    'calm': '#b6f0c4',        # soft green
    'exhausted': '#a9a9a9',   # muted gray
    'anxious': '#ffaf85',     # light orange
    'neutral': '#ffffff',     # default white
}

# synonyms and variants for simple normalization
EMOTION_SYNONYMS = {
    'angry': {'angry', 'mad', 'furious', 'rage'},
    'sad': {'sad', 'depressed', 'miserable', 'lonely', 'alone'},
    'happy': {'happy', 'joy', 'joyful', 'glad', 'excited'},
    'calm': {'calm', 'peaceful', 'relaxed', 'serene'},
    'exhausted': {'exhausted', 'tired', 'sleepy', 'drained'},
    'anxious': {'anxious', 'anxiety', 'worried', 'nervous', 'panic'},
}


def normalize_emotion(emotion_input: str) -> str:
    """Return a canonical emotion like 'sad' or 'angry' for a free-text input."""
    lower = (emotion_input or '').strip().lower()
    if not lower:
        return 'neutral'
    # exact match or synonyms
    for canon, synonyms in EMOTION_SYNONYMS.items():
        if lower == canon or lower in synonyms:
            return canon
    # substring matching
    for canon, synonyms in EMOTION_SYNONYMS.items():
        if any(s in lower for s in synonyms) or canon in lower:
            return canon
    return 'neutral'


def emotion_to_color(emotion_input: str):
    """Return (canonical_emotion, hex_color)"""
    canon = normalize_emotion(emotion_input)
    color = EMOTION_COLOR_MAP.get(canon, EMOTION_COLOR_MAP['neutral'])
    return canon, color