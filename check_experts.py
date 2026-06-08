import urllib.request
import urllib.parse
import json

# Login as admin
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

print("=" * 60)
print("ПРОВЕРКА ФУНКЦИОНАЛА ЭКСПЕРТОВ")
print("=" * 60)

# 1. Check existing experts
req = urllib.request.Request('http://localhost:8888/api/admin/users?role=expert', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    experts = json.loads(response.read())

print("\n1. ЭКСПЕРТЫ В СИСТЕМЕ:")
print("-" * 40)
print("   Всего экспертов:", len(experts))
for e in experts:
    print("   - ID=%s: %s (approved=%s)" % (e['id'], e['username'], e.get('is_approved_expert', False)))

# 2. Check competitions
req = urllib.request.Request('http://localhost:8888/api/admin/competitions', headers={'Authorization': f'Bearer {admin_token}'})
with urllib.request.urlopen(req) as response:
    competitions = json.loads(response.read())

print("\n2. СОРЕВНОВАНИЯ:")
print("-" * 40)
print("   Всего соревнований:", len(competitions))
for c in competitions:
    print("   - ID=%s: %s (direction_id=%s)" % (c['id'], c['name'], c.get('direction_id')))

# 3. Check expert assignments (who is assigned to which competition)
print("\n3. НАЗНАЧЕНИЯ ЭКСПЕРТОВ:")
print("-" * 40)

# We need to check the database for expert_assignments table
# But we can use the expert API to see

# For now, let's just check if there are any expert assignments
# by trying to get competitions for an expert

if experts:
    expert = experts[0]
    print("   Проверяем эксперта: %s (ID=%s)" % (expert['username'], expert['id']))
    
    # Try to login as expert - but we need password
    # Let's just note that we need to create test data
    
print("\n4. ЧТО НУЖНО СДЕЛАТЬ:")
print("-" * 40)
print("   - Создать эксперта (через админ-панель)")
print("   - Назначить эксперта к соревнованию")
print("   - Проверить вход под экспертом")
print("   - Проверить видимость соревнований")
print("   - Проверить выставление баллов")

print("\n" + "=" * 60)
print("ТЕКУЩИЙ ПОТОК РАБОТЫ ЭКСПЕРТА:")
print("=" * 60)
print("""
1. АДМИН создаёт пользователя с ролью 'expert'
2. МЕНЕДЖЕР одобряет заявку эксперта (или напрямую назначает)
3. ЭКСПЕРТ получает доступ к соревнованию через ExpertAssignment
4. ЭКСПЕРТ может:
   - Видеть свои соревнования
   - Выставлять баллы участникам
5. CHIEF_EXPERT может дополнительно:
   - Редактировать задания
   - Управлять экспертами
""")
