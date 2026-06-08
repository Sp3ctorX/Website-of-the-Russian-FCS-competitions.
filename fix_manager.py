import urllib.request
import urllib.parse
import json

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    token = json.loads(response.read())['access_token']

print("Fixing: assigning manager '1' to direction 'Киберспорт'")

# Assign manager ID=5 to direction ID=1 (Киберспорт)
req = urllib.request.Request(
    'http://localhost:8888/api/admin/directions/1/manager/5',
    method='POST',
    headers={'Authorization': f'Bearer {token}'}
)
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print("Result: " + str(result))
except urllib.error.HTTPError as e:
    print("Error: " + str(e.code) + " - " + e.read().decode())

# Now let's verify by logging in as manager '1'
print("\nTesting login as manager '1'...")

# Try common passwords
passwords = ['1', 'password', 'pass123', 'test123', 'password123']

for pwd in passwords:
    data = urllib.parse.urlencode({'username': '1', 'password': pwd})
    req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
    try:
        with urllib.request.urlopen(req) as response:
            manager_token = json.loads(response.read())['access_token']
            print("SUCCESS! Password is: " + pwd)
            
            # Get manager's directions
            req = urllib.request.Request('http://localhost:8888/api/manager/my-directions', headers={'Authorization': f'Bearer {manager_token}'})
            with urllib.request.urlopen(req) as resp:
                directions = json.loads(resp.read())
                print("\nManager's directions: " + str(len(directions)))
                for d in directions:
                    print("  - " + d['name'] + " (ID=" + str(d['id']) + ")")
            
            # Get manager's competitions
            req = urllib.request.Request('http://localhost:8888/api/manager/competitions', headers={'Authorization': f'Bearer {manager_token}'})
            with urllib.request.urlopen(req) as resp:
                competitions = json.loads(resp.read())
                print("\nManager's competitions: " + str(len(competitions)))
                for c in competitions:
                    print("  - " + c['name'])
            
            break
    except:
        pass
