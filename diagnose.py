import urllib.request
import urllib.parse
import json

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    token = json.loads(response.read())['access_token']

print("=" * 50)
print("DIAGNOSTIC DATA")
print("=" * 50)

# 1. Get all directions
req = urllib.request.Request('http://localhost:8888/api/admin/directions', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    directions = json.loads(response.read())

print("\nDIRECTIONS:")
print("-" * 30)
direction_map = {}
for d in directions:
    direction_map[d['id']] = d['name']
    manager_status = "MANAGER: %s" % d.get('manager_id') if d.get('manager_id') else "NO MANAGER"
    print("  ID=%s: %s -> %s" % (d['id'], d['name'], manager_status))

# 2. Get all competitions
req = urllib.request.Request('http://localhost:8888/api/admin/competitions', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())

print("\nCOMPETITIONS:")
print("-" * 30)
for c in competitions:
    dir_name = direction_map.get(c.get('direction_id'), 'UNKNOWN')
    print("  ID=%s: '%s' -> direction_id=%s (%s)" % (c['id'], c['name'], c.get('direction_id'), dir_name))

# 3. Get all managers
req = urllib.request.Request('http://localhost:8888/api/admin/users?role=manager', headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as response:
    managers = json.loads(response.read())

print("\nMANAGERS:")
print("-" * 30)
for m in managers:
    print("  ID=%s: %s (%s)" % (m['id'], m['username'], m.get('full_name', 'no name')))

# 4. Analyze the problem
print("\n" + "=" * 50)
print("ANALYSIS:")
print("=" * 50)

# Find which direction has which manager
for d in directions:
    if d.get('manager_id'):
        print("\n[OK] Direction '%s' (ID=%s) has manager ID=%s" % (d['name'], d['id'], d['manager_id']))
        # Find competitions for this direction
        comps_for_dir = [c for c in competitions if c.get('direction_id') == d['id']]
        if comps_for_dir:
            print("  -> Competitions for this direction: %s" % len(comps_for_dir))
            for comp in comps_for_dir:
                print("    - %s" % comp['name'])
        else:
            print("  -> NO COMPETITIONS for this direction!")
    else:
        print("\n[ERROR] Direction '%s' (ID=%s) has NO MANAGER" % (d['name'], d['id']))

# Check if there are competitions without manager
print("\nSUMMARY:")
print("  Total directions: %s" % len(directions))
print("  Total competitions: %s" % len(competitions))
print("  Total managers: %s" % len(managers))

# Test login as first manager
if managers:
    m = managers[0]
    print("\n" + "=" * 50)
    print("TESTING MANAGER LOGIN:")
    print("=" * 50)
    print("  Manager: %s (ID=%s)" % (m['username'], m['id']))
    
    # We need to find the password - let's try common ones
    # Actually, let's just test the API endpoint
    # First get manager's directions
    # This would require manager login, but we can check directly
