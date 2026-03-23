import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kylaaaa.settings')
django.setup()
from freedom.forms import VentForm

tests = [
    {'text': "I'm sad and tired", 'emotion': ''},
    {'text': "sad I'm tired", 'emotion': ''},
    {'text': "I am anxious and worried", 'emotion': ''},
    {'text': "Hello, I feel strange", 'emotion': ''},
    {'text': "I'm Excited!", 'emotion': ''},
    {'text': "", 'emotion': ''},
    {'text': "I'm Happy", 'emotion': 'happy'},
]

for data in tests:
    f = VentForm(data)
    valid = f.is_valid()
    print('input:', data)
    print('  valid:', valid)
    print('  errors:', f.errors)
    print('  cleaned:', getattr(f, 'cleaned_data', None))
    print('---')
