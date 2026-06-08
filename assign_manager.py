import urllib.request
import urllib.parse
import json

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    token = json.loads(response.read())['access_token']

# Get directions to find first direction
req = urllib.request.Request('http://localhost:8888/api/admin/directions', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    directions = json.loads(response.read())

# Get users to find manager_test
req = urllib.request.Request('http://localhost:8888/api/admin/users', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    users = json.loads(response.read())

# Find manager_test user
manager_user = next((u for u in users if u['username'] == 'manager_test'), None)
if manager_user:
    print(f'Found manager: {manager_user["username"]} (id: {manager_user["id"]})')
    
    # Assign manager to first direction
    if directions:
        direction = directions[0]
        print(f'Assigning manager to direction: {direction["name"]} (id: {direction["id"]})')
        
        req = urllib.request.Request(
            f'http://localhost:8888/api/admin/directions/{direction["id"]}/manager/{manager_user["id"]}',
            method='POST',
            headers={'Authorization': f'Bearer {token}'}
        )
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read())
                print(f'Result: {result}')
        except urllib.error.HTTPError as e:
            print(f'Error: {e.code} - {e.read().decode()}')
else:
    print('Manager user not found')
