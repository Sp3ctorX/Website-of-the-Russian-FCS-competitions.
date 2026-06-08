import urllib.request
import urllib.parse
import json

print("=" * 60)
print("ТЕСТ: НАЗНАЧЕНИЕ ЭКСПЕРТА ЧЕРЕЗ АДМИН API")
print("=" * 60)

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

# Get competitions
req = urllib.request.Request('http://localhost:8888/api/admin/competitions', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())

print("\n1. Competitions:")
for c in competitions:
    print("   ID=%s: %s" % (c['id'], c['name']))

# Get experts
req = urllib.request.Request('http://localhost:8888/api/admin/users?role=expert', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    experts = json.loads(response.read())

print("\n2. Experts:")
for e in experts:
    print("   ID=%s: %s" % (e['id'], e['username']))

# Assign expert to competition
if competitions and experts:
    competition_id = competitions[0]['id']
    expert_id = experts[0]['id']
    
    print("\n3. Assigning expert %s to competition %s..." % (expert_id, competition_id))
    
    req = urllib.request.Request(
        'http://localhost:8888/api/admin/assign-expert/%s/to-competition/%s' % (expert_id, competition_id),
        method='POST',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            print("   SUCCESS: %s" % result['message'])
    except urllib.error.HTTPError as e:
        print("   ERROR: %s - %s" % (e.code, e.read().decode()))

# Test expert login
print("\n4. Testing expert login...")

data = urllib.parse.urlencode({'username': 'test_expert', 'password': 'expert123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
try:
    with urllib.request.urlopen(req) as response:
        expert_token = json.loads(response.read())['access_token']
        print("   Login: OK")
        
        req = urllib.request.Request('http://localhost:8888/api/expert/my-competitions', headers={'Authorization': f'Bearer {expert_token}'})
        with urllib.request.urlopen(req) as resp:
            comps = json.loads(resp.read())
            print("   Competitions: %s" % len(comps))
            for c in comps:
                print("   - %s" % c['name'])
except urllib.error.HTTPError as e:
    print("   Error: %s" % e.read().decode())

print("\n" + "=" * 60)
