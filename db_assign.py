# Direct database access to assign expert
from app.database import SessionLocal
from app.models import ExpertAssignment, User, Competition
from datetime import datetime

db = SessionLocal()

# Check if expert assignment already exists
existing = db.query(ExpertAssignment).filter(
    ExpertAssignment.user_id == 6,
    ExpertAssignment.competition_id == 1
).first()

if existing:
    print('Expert already assigned!')
else:
    # Create assignment
    assignment = ExpertAssignment(
        user_id=6,
        competition_id=1,
        is_chief=False,
        assigned_by=1,
        assigned_at=datetime.utcnow()
    )
    db.add(assignment)
    db.commit()
    print('Expert assigned! ID:', assignment.id)

db.close()
