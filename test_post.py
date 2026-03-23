import urllib.request, urllib.parse

url = 'http://127.0.0.1:8000/'
data = urllib.parse.urlencode({'text': "I'm angry and upset", 'emotion': ''}).encode()
req = urllib.request.Request(url, data=data)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode()
    print('status', resp.status)
    print('has_angry_tag', '<strong>angry</strong>' in html)
    print(html[:800])
