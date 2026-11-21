from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.goal import Goal
from app.models.bmi_record import BmiRecord
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(payload: GoalCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = Goal(user_id=user.id, **payload.model_dump())
    db.add(goal); db.commit(); db.refresh(goal)
    return goal


@router.get("", response_model=list[GoalResponse])
def list_goals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Goal).filter(Goal.user_id == user.id).order_by(Goal.created_at.desc()).all()


@router.get("/progress")
def goal_progress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.user_id == user.id, Goal.is_active.is_(True)).order_by(Goal.created_at.desc()).first()
    latest = db.query(BmiRecord).filter(BmiRecord.user_id == user.id).order_by(BmiRecord.measured_at.desc()).first()
    if not goal:
        return {"available": False, "message": "No active goal found."}
    if not latest:
        return {"available": False, "message": "Add a BMI record to calculate goal progress."}
    return {
        "available": True, "goal": goal,
        "current_weight_kg": latest.weight_kg,
        "target_weight_kg": goal.target_weight_kg,
        "remaining_kg": round(latest.weight_kg - goal.target_weight_kg, 2),
        "is_target_reached": abs(latest.weight_kg - goal.target_weight_kg) < 0.1
    }


@router.patch("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, payload: GoalUpdate, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(goal, key, value)
    db.commit(); db.refresh(goal)
    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal); db.commit()
    return None


