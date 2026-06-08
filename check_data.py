import urllib.request
import urllib.parse
import json

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    token = json.loads(response.read())['access_token']

print('Token received')

# Get all users
req = urllib.request.Request('http://localhost:8888/api/admin/users', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    users = json.loads(response.read())
    print('Users:')
    for u in users:
        print(f'  - {u["username"]}: {u["role"]}')

# Get directions
req = urllib.request.Request('http://localhost:8888/api/admin/directions', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    directions = json.loads(response.read())
    print('\nDirections:')
    for d in directions:
        print(f'  - {d["name"]} (manager_id: {d.get("manager_id")})')
