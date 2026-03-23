import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kylaaaa.settings')
django.setup()
from django.test import Client

c = Client()
resp = c.post('/', {'text': "I'm angry and upset", 'emotion': ''}, follow=True)
print('status_code', resp.status_code)
html = resp.content.decode()
print('has_angry_tag', '<strong>angry</strong>' in html)
print(html[:800])
