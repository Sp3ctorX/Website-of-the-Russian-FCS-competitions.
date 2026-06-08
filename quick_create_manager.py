import urllib.request
import urllib.parse
import json

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    token = json.loads(response.read())['access_token']

print('Logged in as admin')

# Create a new manager
user_data = json.dumps({
    'username': 'newmanager',
    'email': 'newmanager@test.com',
    'full_name': 'Новый Менеджер',
    'password': 'password123',
    'role': 'manager'
}).encode()

req = urllib.request.Request(
    'http://localhost:8888/api/admin/users',
    data=user_data,
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print(f'SUCCESS: Manager created - {result["username"]} (role: {result["role"]}, id: {result["id"]})')
except urllib.error.HTTPError as e:
    print(f'Error: {e.code} - {e.read().decode()}')
