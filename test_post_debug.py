import urllib.request, urllib.parse, re, sys

url = 'http://127.0.0.1:8000/'
print('GET', url)
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode()
        headers = resp.getheaders()
        set_cookie = dict(headers).get('Set-Cookie', '')
        print('got GET, len(html)=', len(html))
        print('set-cookie:', set_cookie)
except Exception as e:
    print('GET failed', e)
    sys.exit(1)

m = re.search(r"name=['\"]csrfmiddlewaretoken['\"]\s+value=['\"]([^'\"]+)['\"]", html)
print('found token in HTML?', bool(m))
if not m:
    print('first 500 chars:', html[:500])
    sys.exit(1)
token = m.group(1)
print('token len', len(token), 'token sample', token[:10])

m2 = re.search(r'csrftoken=([^;]+)', set_cookie)
csrftoken = m2.group(1) if m2 else ''
print('csrftoken cookie present?', bool(csrftoken))

post_data = {'text': "I'm angry and upset", 'emotion': '', 'csrfmiddlewaretoken': token}
print('POSTing data keys:', post_data.keys())

data = urllib.parse.urlencode(post_data).encode()
req = urllib.request.Request(url, data=data)
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
if csrftoken:
    req.add_header('Cookie', f'csrftoken={csrftoken}')
req.add_header('Referer', url)

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode()
        print('status', resp.status)
        print('has_angry_tag', '<strong>angry</strong>' in html)
        print(html[:800])
except urllib.error.HTTPError as e:
    print('HTTPError', e.code, e.reason)
    print(e.read().decode())
except Exception as e:
    print('other error', e)
