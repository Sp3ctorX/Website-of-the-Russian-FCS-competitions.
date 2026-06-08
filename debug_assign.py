import urllib.request
import urllib.parse
import json

print("=" * 60)
print("ОТЛАДКА: НАЗНАЧЕНИЕ ЭКСПЕРТА")
print("=" * 60)

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

# Login as manager
data = urllib.parse.urlencode({'username': '1', 'password': '1'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    manager_token = json.loads(response.read())['access_token']

# Get manager's competitions
req = urllib.request.Request('http://localhost:8888/api/manager/competitions', headers={'Authorization': f'Bearer {manager_token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())

print("Competitions:")
for c in competitions:
    print("  ID=%s: %s (direction_id=%s)" % (c['id'], c['name'], c.get('direction_id')))

# Get experts
req = urllib.request.Request('http://localhost:8888/api/admin/users?role=expert', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    experts = json.loads(response.read())

print("\nExperts:")
for e in experts:
    print("  ID=%s: %s (approved=%s)" % (e['id'], e['username'], e.get('is_approved_expert', False)))

if competitions and experts:
    competition_id = competitions[0]['id']
    expert_id = experts[0]['id']
    
    print("\nTrying to assign expert %s to competition %s..." % (expert_id, competition_id))
    
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
