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