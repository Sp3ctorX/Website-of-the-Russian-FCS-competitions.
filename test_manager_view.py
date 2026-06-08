import urllib.request
import urllib.parse
import json

# Test manager login
print("=" * 50)
print("TESTING MANAGER LOGIN")
print("=" * 50)

# Get all managers first
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

req = urllib.request.Request('http://localhost:8888/api/admin/users?role=manager', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    managers = json.loads(response.read())

print("\nAvailable managers:")
for m in managers:
    print("  ID=%s: %s" % (m['id'], m['username']))

# Try to login as each manager and test their competitions
# But we need passwords... Let me create a test competition for direction ID=1 first

# Let's check the problem from another angle
# Get the manager's directions directly using admin token to simulate

print("\n" + "=" * 50)
print("CHECKING MANAGER VIEW (using admin to simulate)")
print("=" * 50)

for m in managers:
    print("\nManager: %s (ID=%s)" % (m['username'], m['id']))
    
    # Get directions for this manager
    # Using admin to check would need a different API
    # Let's just list what we found earlier
    
print("\nBased on earlier data:")
print("  Manager ID=2 (manager_test) -> Direction ID=1 (Kiberспорт)")
print("    Competitions: 4 (all for direction_id=1)")
print("  Manager ID=3 (newmanager) -> Direction ID=2")
print("    Competitions: 1")
print("  Manager ID=4 (men)")
print("    NO DIRECTION ASSIGNED!")
print("  Manager ID=5 (1)")
print("    Direction ID=5, NO competitions")

print("\n" + "=" * 50)
print("POSSIBLE ISSUE:")
print("=" * 50)
print("User might be logging in as:")
print("  - manager ID=4 (men) - has NO direction assigned!")
print("  - manager ID=5 (1) - direction has NO competitions!")
print("  - NEW manager that was just created - needs direction assignment")
