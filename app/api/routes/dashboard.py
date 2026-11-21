from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.bmi_record import BmiRecord
from app.models.goal import Goal

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def get_dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(BmiRecord).filter(BmiRecord.user_id == user.id).order_by(BmiRecord.measured_at.desc()).limit(2).all()
    active_goal = db.query(Goal).filter(Goal.user_id == user.id, Goal.is_active.is_(True)).order_by(Goal.created_at.desc()).first()
    latest = records[0] if records else None
    previous = records[1] if len(records) > 1 else None
    return {
        "user": {"id": user.id, "name": user.name, "email": user.email},
        "latest_record": latest,
        "previous_record": previous,
        "bmi_change": round(latest.bmi - previous.bmi, 2) if latest and previous else None,
        "active_goal": active_goal,
        "total_records": db.query(BmiRecord).filter(BmiRecord.user_id == user.id).count()
    }
