import urllib.request
import urllib.parse
import json

print("=" * 60)
print("ТЕСТ: НАЗНАЧЕНИЕ ЭКСПЕРТА К СОРЕВНОВАНИЮ")
print("=" * 60)

# Login as admin to get experts
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

# Get experts
req = urllib.request.Request('http://localhost:8888/api/admin/users?role=expert', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    experts = json.loads(response.read())

print("1. Экспертов в системе: %s" % len(experts))
if not experts:
    print("   Создаём эксперта...")
    
    expert_data = json.dumps({
        'username': 'test_expert',
        'email': 'expert@test.com',
        'full_name': 'Тестовый Эксперт',
        'password': 'expert123',
        'role': 'expert'
    }).encode()

    req = urllib.request.Request(
        'http://localhost:8888/api/admin/users',
        data=expert_data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {admin_token}'
        }
    )
    with urllib.request.urlopen(req) as response:
        expert = json.loads(response.read())
        expert_id = expert['id']
        print("   Создан: test_expert (ID=%s)" % expert_id)
else:
    expert_id = experts[0]['id']
    print("   Первый эксперт: ID=%s" % expert_id)

# Login as manager
data = urllib.parse.urlencode({'username': '1', 'password': '1'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    manager_token = json.loads(response.read())['access_token']

print("\n2. Вход под менеджером: OK")

# Get competitions for this manager
req = urllib.request.Request('http://localhost:8888/api/manager/competitions', headers={'Authorization': f'Bearer {manager_token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())

print("   Соревнований менеджера: %s" % len(competitions))
if competitions:
    competition_id = competitions[0]['id']
    print("   Используем соревнование ID=%s: %s" % (competition_id, competitions[0]['name']))

# Assign expert to competition
if competitions:
    print("\n3. Назначение эксперта к соревнованию...")
    
    req = urllib.request.Request(
        'http://localhost:8888/api/manager/competitions/%s/assign-expert/%s' % (competition_id, expert_id),
        method='POST',
        headers={'Authorization': f'Bearer {manager_token}'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            print("   Результат: %s" % result['message'])
    except urllib.error.HTTPError as e:
        print("   Ошибка: %s" % e.read().decode())

# Now test login as expert
print("\n4. Тест входа под экспертом...")

data = urllib.parse.urlencode({'username': 'test_expert', 'password': 'expert123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
try:
    with urllib.request.urlopen(req) as response:
        expert_token = json.loads(response.read())['access_token']
        print("   Вход: OK")
        
        # Get expert's competitions
        req = urllib.request.Request('http://localhost:8888/api/expert/my-competitions', headers={'Authorization': f'Bearer {expert_token}'})
        with urllib.request.urlopen(req) as resp:
            comps = json.loads(resp.read())
            print("   Соревнований: %s" % len(comps))
            for c in comps:
                print("   - %s" % c['name'])
            
        # Get tasks
        req = urllib.request.Request('http://localhost:8888/api/expert/tasks', headers={'Authorization': f'Bearer {expert_token}'})
        with urllib.request.urlopen(req) as resp:
            tasks = json.loads(resp.read())
            print("   Заданий: %s" % len(tasks))
            
except urllib.error.HTTPError as e:
    print("   Ошибка: %s" % e.read().decode())

print("\n" + "=" * 60)
print("ГОТОВО!")
print("=" * 60)
print("""
Теперь эксперт может:
- Видеть свои соревнования
- Выставлять баллы участникам
- Редактировать задания (если chief_expert)

Данные для входа:
- Эксперт: test_expert / expert123
- Менеджер: 1 / 1
""")
