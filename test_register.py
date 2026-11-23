import json, urllib.request, sys

data = {
    "email": "testuser@example.com",
    "password": "StrongPass123!",
    "role": "CANDIDATE",
    "full_name": "Test User"
}
body = json.dumps(data).encode('utf-8')
req = urllib.request.Request(
    url='http://127.0.0.1:8001/api/v1/auth/register',
    data=body,
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('Error', e.code, e.read().decode())
except Exception as e:
    print('Exception', e)
