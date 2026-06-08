import urllib.request
import urllib.parse
import json

print("=" * 60)
print("ИСПРАВЛЕНИЕ: НАЗНАЧЕНИЕ ЭКСПЕРТА")
print("=" * 60)

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

# Get all users to see what's going on
req = urllib.request.Request('http://localhost:8888/api/admin/users', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    users = json.loads(response.read())

print("All users:")
for u in users:
    print("  ID=%s: %s (role=%s, approved=%s)" % (u['id'], u['username'], u['role'], u.get('is_approved_expert', False)))

# Find the test_expert
test_expert = None
for u in users:
    if u['username'] == 'test_expert':
        test_expert = u
        break

if test_expert:
    print("\nTest expert: role=%s" % test_expert['role'])
    
    # If role is not expert, we need to promote them
    if test_expert['role'] != 'expert':
        print("Promoting user to expert...")
        req = urllib.request.Request(
            'http://localhost:8888/api/admin/users/%s/promote' % test_expert['id'],
            method='POST',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        try:
            with urllib.request.urlopen(req) as response:
                print("Promoted!")
        except:
            pass

# Login as manager
data = urllib.parse.urlencode({'username': '1', 'password': '1'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    manager_token = json.loads(response.read())['access_token']

# Get manager's first competition
req = urllib.request.Request('http://localhost:8888/api/manager/competitions', headers={'Authorization': f'Bearer {manager_token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())

if competitions and test_expert:
    competition_id = competitions[0]['id']
    expert_id = test_expert['id']
    
    print("\nAssigning expert %s to competition %s..." % (expert_id, competition_id))
    
    req = urllib.request.Request(
        'http://localhost:8888/api/manager/competitions/%s/assign-expert/%s' % (competition_id, expert_id),
        method='POST',
        headers={'Authorization': f'Bearer {manager_token}'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            print("SUCCESS: %s" % result)
    except urllib.error.HTTPError as e:
        print("HTTP Error %s: %s" % (e.code, e.read().decode()))

# Test expert login
print("\nTesting expert login...")
data = urllib.parse.urlencode({'username': 'test_expert', 'password': 'expert123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
try:
    with urllib.request.urlopen(req) as response:
        expert_token = json.loads(response.read())['access_token']
        print("Expert login: OK")
        
        req = urllib.request.Request('http://localhost:8888/api/expert/my-competitions', headers={'Authorization': f'Bearer {expert_token}'})
        with urllib.request.urlopen(req) as resp:
            comps = json.loads(resp.read())
            print("Competitions: %s" % len(comps))
            for c in comps:
                print("  - %s" % c['name'])
except urllib.error.HTTPError as e:
    print("Error: %s" % e.read().decode())
