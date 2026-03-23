from django import forms
from django.core.exceptions import ValidationError
import re

from .utils import normalize_emotion


class VentForm(forms.Form):
    emotion = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'e.g., sad, angry, exhausted',
        'list': 'emotions',
    }), label='How do you feel?')

    text = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5,
        'placeholder': "Start with \"I'm sad\" — then vent. What's on your mind?"
    }), label='')

    def clean(self):
        cleaned = super().clean()
        text = (cleaned.get('text') or '').strip()
        emotion = (cleaned.get('emotion') or '').strip()

        # Try to extract emotion from the start of the text, e.g. "I'm sad" or "I am angry" or leading word
        extracted = None
        m = re.match(r"^\s*(?:i(?:'m| am)\s+)([a-zA-Z]+)\b", text, re.I)
        if m:
            extracted = m.group(1)
        else:
            m2 = re.match(r"^\s*([a-zA-Z]+)\b", text)
            if m2:
                # if they simply start with the emotion word ("sad, ..." or "sad I'm ...") capture it
                extracted = m2.group(1)

        if not emotion and extracted:
            canon = normalize_emotion(extracted)
            if canon == 'neutral':
                raise ValidationError("Please start your vent by stating how you feel (e.g., \"I'm sad\") or fill the 'How do you feel?' field.")
            cleaned['emotion'] = canon
        elif emotion:
            canon = normalize_emotion(emotion)
            if canon == 'neutral':
                raise ValidationError("Unknown emotion. Please use simple emotions like 'sad', 'angry', 'calm', 'happy', 'exhausted', or 'anxious'.")
            cleaned['emotion'] = canon
        else:
            # neither provided nor extractable
            raise ValidationError("Please start your vent by stating how you feel (e.g., \"I'm sad\") or fill the 'How do you feel?' field.")

        return cleaned