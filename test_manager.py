import urllib.request
import urllib.parse
import json

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    token = json.loads(response.read())['access_token']

# Create a competition for direction 1 (where manager is assigned)
competition_data = json.dumps({
    'name': 'Тестовое соревнование',
    'direction_id': 1,
    'description': 'Тестовое соревнование для проверки',
    'date': '2026-04-01T10:00:00',
    'location': 'Москва'
}).encode()

req = urllib.request.Request(
    'http://localhost:8888/api/admin/competitions',
    data=competition_data,
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
)
try:
    with urllib.request.urlopen(req) as response:
        competition = json.loads(response.read())
        print(f'Competition created: {competition["name"]} (id: {competition["id"]})')
except urllib.error.HTTPError as e:
    print(f'Error: {e.code} - {e.read().decode()}')

# Now test as manager
print('\n--- Testing as manager ---')
data = urllib.parse.urlencode({'username': 'manager_test', 'password': 'test123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    manager_token = json.loads(response.read())['access_token']

# Get manager's directions
req = urllib.request.Request('http://localhost:8888/api/manager/my-directions', headers={'Authorization': f'Bearer {manager_token}'})
with urllib.request.urlopen(req) as response:
    directions = json.loads(response.read())
    print(f'Manager directions: {len(directions)}')
    for d in directions:
        print(f'  - {d["name"]} (id: {d["id"]})')

# Get manager's competitions
req = urllib.request.Request('http://localhost:8888/api/manager/competitions', headers={'Authorization': f'Bearer {manager_token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())
    print(f'\nManager competitions: {len(competitions)}')
    for c in competitions:
        print(f'  - {c["name"]}')
