import urllib.request
import urllib.parse
import json
import time

print("=" * 60)
print("ОЖИДАНИЕ ПЕРЕЗАГРУЗКИ СЕРВЕРА...")
print("=" * 60)

# Wait for server to reload
time.sleep(3)

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

print("Logged in as admin")

# Try to assign expert to competition
expert_id = 6
competition_id = 1

print("Assigning expert %s to competition %s..." % (expert_id, competition_id))

req = urllib.request.Request(
    'http://localhost:8888/api/admin/assign-expert/%s/to-competition/%s' % (expert_id, competition_id),
    method='POST',
    headers={'Authorization': 'Bearer ' + admin_token}
)
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print("SUCCESS: %s" % result['message'])
except urllib.error.HTTPError as e:
    print("ERROR %s: %s" % (e.code, e.read().decode()))

# Test expert login
print("\nTesting expert login...")

data = urllib.parse.urlencode({'username': 'test_expert', 'password': 'expert123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
try:
    with urllib.request.urlopen(req) as response:
        expert_token = json.loads(response.read())['access_token']
        print("Expert login: OK")
        
        req = urllib.request.Request('http://localhost:8888/api/expert/my-competitions', headers={'Authorization': 'Bearer ' + expert_token})
        with urllib.request.urlopen(req) as resp:
            comps = json.loads(resp.read())
            print("Competitions: %s" % len(comps))
            for c in comps:
                print("  - %s" % c['name'])
except urllib.error.HTTPError as e:
    print("Error: %s" % e.read().decode())
