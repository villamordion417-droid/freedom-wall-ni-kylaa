import urllib.request, urllib.parse, re

url = 'http://127.0.0.1:8000/'

# GET the form page to obtain CSRF token and cookie
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode()
    headers = resp.getheaders()
    set_cookie = dict(headers).get('Set-Cookie', '')

# extract csrf token from hidden input
m = re.search(r"name=['\"]csrfmiddlewaretoken['\"]\s+value=['\"]([^'\"]+)['\"]", html)
if not m:
    print('could not find csrf token in form')
    print(html[:800])
    raise SystemExit(1)
token = m.group(1)

# extract csrftoken from set-cookie header if present
m2 = re.search(r'csrftoken=([^;]+)', set_cookie)
csrftoken = m2.group(1) if m2 else ''

data = urllib.parse.urlencode({'text': "I'm angry and upset", 'emotion': '', 'csrfmiddlewaretoken': token}).encode()
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
