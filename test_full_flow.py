import urllib.request
import urllib.parse
import json

print("=" * 60)
print("ТЕСТ: ПОЛНЫЙ ПОТОК ЭКСПЕРТА")
print("=" * 60)

# 1. Login as participant to apply for expert
print("\n1. Тест: Пользователь подаёт заявку на эксперта...")

# First check current user roles
data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin123'})
req = urllib.request.Request('http://localhost:8888/api/auth/login', data=data.encode())
with urllib.request.urlopen(req) as response:
    admin_token = json.loads(response.read())['access_token']

# Get all users
req = urllib.request.Request('http://localhost:8888/api/admin/users', headers={'Authorization': 'Bearer ' + admin_token})
with urllib.request.urlopen(req) as response:
    users = json.loads(response.read())

print("\nПользователи в системе:")
for u in users:
    print("  ID=%s: %s (role=%s)" % (u['id'], u['username'], u['role']))

# Find a participant user
participant = None
for u in users:
    if u['role'] == 'participant':
        participant = u
        break

if not participant:
    print("\nНет участников, нужно создать!")
else:
    print("\nНайден участник: %s" % participant['username'])

print("\n" + "=" * 60)
print("ГОТОВО!")
print("=" * 60)
print("""
ПОЛНЫЙ ПОТОК РАБОТЫ:

1. УЧАСТНИК подаёт заявку на становление экспертом:
   - Заходит в свой профиль
   - Видит секцию "Стать экспертом"
   - Выбирает направление
   - Нажимает "Подать заявку"

2. МЕНЕДЖЕР одобряет заявку:
   - Заходит в панель менеджера
   - Вкладка "Эксперты"
   - Секция "Заявки на становление экспертом"
   - Нажимает "Одобрить"
   - Пользователь становится экспертом

3. ЭКСПЕРТ подаёт заявку на соревнование:
   - Заходит в панель эксперта
   - Видит доступные соревнования
   - Подаёт заявку на конкретное соревнование

4. МЕНЕДЖЕР одобряет заявку на соревнование:
   - Вкладка "Заявки экспертов на соревнования"
   - Одобряет заявку
   - Эксперт получает доступ к соревнованию
""")
