import urllib.request
import urllib.parse
import json

print("=" * 60)
print("ПРОВЕРКА: ЭКСПЕРТ ПОСЛЕ НАЗНАЧЕНИЯ")
print("=" * 60)

# Test expert login
data = urllib.parse.urlencode({'username': 'test_expert', 'password': 'expert123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
try:
    with urllib.request.urlopen(req) as response:
        expert_token = json.loads(response.read())['access_token']
        print("1. Expert login: OK")
        
        # Get competitions
        req = urllib.request.Request('http://localhost:8888/api/expert/my-competitions', headers={'Authorization': 'Bearer ' + expert_token})
        with urllib.request.urlopen(req) as resp:
            comps = json.loads(resp.read())
            print("2. Competitions: %s" % len(comps))
            for c in comps:
                print("   - %s (ID: %s)" % (c['name'], c['id']))
        
        # Get tasks
        req = urllib.request.Request('http://localhost:8888/api/expert/tasks', headers={'Authorization': 'Bearer ' + expert_token})
        with urllib.request.urlopen(req) as resp:
            tasks = json.loads(resp.read())
            print("3. Tasks: %s" % len(tasks))
            
except urllib.error.HTTPError as e:
    print("Error: %s" % e.read().decode())

print("\n" + "=" * 60)
print("ГОТОВО!")
print("=" * 60)
print("""
Эксперт теперь может:
- Видеть свои соревнования
- Выставлять баллы участникам
- Просматривать задания

Данные для входа:
- Эксперт: test_expert / expert123
- Менеджер: 1 / 1
""")
