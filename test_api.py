import urllib.request
import urllib.parse
import json

try:
    # Login
    data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
    req = urllib.request.Request(f'http://localhost:8888/api/auth/login', data=data.encode())
    with urllib.request.urlopen(req) as response:
        token = json.loads(response.read())['access_token']
    print('Logged in, token:', token[:20])

    # Create user
    user_data = json.dumps({
        'username': 'manager_test',
        'email': 'manager_test@test.com',
        'full_name': 'Test Manager',
        'password': 'test123',
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
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print('User created:', result)
except urllib.error.HTTPError as e:
    print('HTTP Error:', e.code, e.read().decode())
except Exception as e:
    print('Error:', e)
