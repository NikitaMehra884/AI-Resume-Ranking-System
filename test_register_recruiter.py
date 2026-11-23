import json, urllib.request

data = {
    "email": "recruiter@example.com",
    "password": "StrongPass123!",
    "role": "RECRUITER",
    "company_name": "Acme Corp"
}
body = json.dumps(data).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8001/api/v1/auth/register', data=body, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('Error', e.code, e.read().decode())
except Exception as e:
    print('Exception', e)
