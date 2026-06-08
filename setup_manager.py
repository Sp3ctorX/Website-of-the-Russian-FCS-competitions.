import urllib.request
import urllib.parse
import json

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    token = json.loads(response.read())['access_token']

# Get directions
req = urllib.request.Request('http://localhost:8888/api/admin/directions', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    directions = json.loads(response.read())

# Find direction 1 (first one without manager)
direction_id = None
for d in directions:
    if not d.get('manager_id'):
        direction_id = d['id']
        break

if direction_id:
    # Assign newmanager to this direction
    req = urllib.request.Request(
        f'http://localhost:8888/api/admin/directions/{direction_id}/manager/3',
        method='POST',
        headers={'Authorization': f'Bearer {token}'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            print(f'SUCCESS: Manager newmanager assigned to direction {direction_id}')
    except urllib.error.HTTPError as e:
        print(f'Error: {e.code} - {e.read().decode()}')
else:
    print('All directions already have managers')

# Create a test competition for direction 1
comp_data = json.dumps({
    'name': 'Тестовое соревнование 2',
    'direction_id': 1,
    'description': 'Для проверки менеджера',
    'date': '2026-05-01T12:00:00',
    'location': 'Онлайн'
}).encode()

req = urllib.request.Request(
    'http://localhost:8888/api/admin/competitions',
    data=comp_data,
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
)

try:
    with urllib.request.urlopen(req) as response:
        comp = json.loads(response.read())
        print(f'SUCCESS: Competition created - {comp["name"]} (id: {comp["id"]})')
except urllib.error.HTTPError as e:
    print(f'Error creating competition: {e.code} - {e.read().decode()}')

print('\n=== Test login as newmanager ===')

# Test login as newmanager
data = urllib.parse.urlencode({'username': 'newmanager', 'password': 'password123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    manager_token = json.loads(response.read())['access_token']
    print('Login as newmanager: SUCCESS')

# Check manager's competitions
req = urllib.request.Request('http://localhost:8888/api/manager/competitions', headers={'Authorization': f'Bearer {manager_token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())
    print(f'Manager sees {len(competitions)} competitions:')
    for c in competitions:
        print(f'  - {c["name"]}')
