from app.database import SessionLocal, engine, Base
from app.models import User, Direction
from app.auth import get_password_hash
from datetime import datetime

Base.metadata.create_all(bind=engine)

db = SessionLocal()

existing_admin = db.query(User).filter(User.username == "admin").first()
if not existing_admin:
    admin = User(
        username="admin",
        email="admin@sait2.ru",
        hashed_password=get_password_hash("admin123"),
        full_name="Главный администратор",
        role="admin",
        is_active=True
    )
    db.add(admin)
    print("Admin user created")

directions_data = [
    {"name": "Киберспорт", "description": "Компьютерные соревнования по популярным дисциплинам", "icon": "🎮"},
    {"name": "Гонки дронов", "description": "Соревнования по скоростному пилотированию дронов", "icon": "🏎️"},
    {"name": "Спортивное программирование", "description": "Решение алгоритмических задач на скорость", "icon": "💻"},
    {"name": "Фиджитал", "description": "Сингапур цифрового и физического спорта", "icon": "🎯"},
]

for d in directions_data:
    existing = db.query(Direction).filter(Direction.name == d["name"]).first()
    if not existing:
        direction = Direction(**d)
        db.add(direction)

db.commit()
db.close()

print("Database initialized!")
print("Admin login: admin / admin123")
