import urllib.request
import urllib.parse
import json

print("=" * 60)
print("СОЗДАНИЕ ТЕСТОВОГО ЭКСПЕРТА")
print("=" * 60)

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

# 1. Create expert
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

try:
    with urllib.request.urlopen(req) as response:
        expert = json.loads(response.read())
        print("\n1. ЭКСПЕРТ СОЗДАН:")
        print("   Логин: test_expert")
        print("   Пароль: expert123")
        print("   ID: %s" % expert['id'])
except urllib.error.HTTPError as e:
    error_msg = e.read().decode()
    print("   Ошибка создания: %s" % error_msg)
    # Expert might already exist, let's find their ID
    req = urllib.request.Request('http://localhost:8888/api/admin/users', headers={'Authorization': f'Bearer {admin_token}'})
    with urllib.request.urlopen(req) as response:
        users = json.loads(response.read())
        for u in users:
            if u['username'] == 'test_expert':
                expert = u
                print("\n1. ЭКСПЕРТ УЖЕ СУЩЕСТВУЕТ:")
                print("   ID: %s" % expert['id'])
                break

expert_id = expert['id']

# 2. Get competitions
req = urllib.request.Request('http://localhost:8888/api/admin/competitions', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())

print("\n2. СОРЕВНОВАНИЯ:")
for c in competitions:
    print("   ID=%s: %s" % (c['id'], c['name']))

# 3. Assign expert to competition (using manager API as admin has all permissions)
# Actually, we need to use the expert API to assign
# Let me check what API to use

# For now, let's just directly assign using admin
# We'll use the expert assignment endpoint

print("\n3. НАЗНАЧЕНИЕ ЭКСПЕРТА К СОРЕВНОВАНИЮ:")

# We need to use the expert router to assign
# POST /api/expert/competitions/{competition_id}/experts
# But this requires chief_expert role

# Let's use the manager endpoint instead or create a direct assignment
# Actually, let me check if we can use the admin to assign

# For now, let's just note that we need a chief_expert to assign
# Or we can directly assign via database

print("   Нужен chief_expert для назначения")
print("   Или нужно создать API для менеджера")

# 4. Test login as expert
print("\n4. ТЕСТ ВХОДА ПОД ЭКСПЕРТОМ:")

data = urllib.parse.urlencode({'username': 'test_expert', 'password': 'expert123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
try:
    with urllib.request.urlopen(req) as response:
        expert_token = json.loads(response.read())['access_token']
        print("   Вход: УСПЕХ")
        
        # Get expert's competitions
        req = urllib.request.Request('http://localhost:8888/api/expert/my-competitions', headers={'Authorization': f'Bearer {expert_token}'})
        with urllib.request.urlopen(req) as resp:
            comps = json.loads(resp.read())
            print("   Соревнований: %s" % len(comps))
            
        # Get expert's tasks
        req = urllib.request.Request('http://localhost:8888/api/expert/tasks', headers={'Authorization': f'Bearer {expert_token}'})
        with urllib.request.urlopen(req) as resp:
            tasks = json.loads(resp.read())
            print("   Заданий: %s" % len(tasks))
            
except urllib.error.HTTPError as e:
    print("   Вход: ОШИБКА - %s" % e.read().decode())

print("\n" + "=" * 60)
print("ВЫВОД:")
print("=" * 60)
print("""
Для полноценной работы эксперта нужно:
1. Создать эксперта (через админ-панель) - РАБОТАЕТ
2. Назначить эксперта к соревнованию
   - Нужен chief_expert ИЛИ
   - Нужно добавить функционал в менеджера
3. Эксперт увидит соревнование в панели

Сейчас эксперт не назначен ни к одному соревнованию!
""")
