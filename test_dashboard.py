import urllib.request
import urllib.parse
import json

print("Testing expert dashboard...")

# Login as expert
data = urllib.parse.urlencode({'username': 'test_expert', 'password': 'expert123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    expert_token = json.loads(response.read())['access_token']

print("Login OK")

# Try to get expert dashboard page
req = urllib.request.Request('http://localhost:8888/expert/dashboard', headers={'Authorization': 'Bearer ' + expert_token})
try:
    with urllib.request.urlopen(req) as response:
        print("Dashboard page: OK (status %s)" % response.status)
except urllib.error.HTTPError as e:
    print("Dashboard page error: %s" % e.code)
