from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.bmi_record import BmiRecord
from app.schemas.bmi import BmiCreate, BmiUpdate, BmiRecordResponse, BmiCalculationResponse
from app.services.bmi_service import calculate_bmi, classify_bmi, healthy_weight_range

router = APIRouter(prefix="/bmi", tags=["BMI"])


@router.post("/calculate", response_model=BmiCalculationResponse)
def calculate(payload: BmiCreate):
    bmi = calculate_bmi(payload.height_cm, payload.weight_kg)
    low, high = healthy_weight_range(payload.height_cm)
    return BmiCalculationResponse(
        bmi=bmi, category=classify_bmi(bmi), healthy_weight_min_kg=low,
        healthy_weight_max_kg=high,
        message="BMI is a screening measure and should not be treated as a medical diagnosis."
    )


@router.post("/records", response_model=BmiRecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(payload: BmiCreate, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    bmi = calculate_bmi(payload.height_cm, payload.weight_kg)
    record = BmiRecord(
        user_id=user.id, height_cm=payload.height_cm, weight_kg=payload.weight_kg,
        bmi=bmi, category=classify_bmi(bmi), note=payload.note,
        measured_at=payload.measured_at or datetime.now(timezone.utc)
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/records", response_model=list[BmiRecordResponse])
def list_records(
    skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200),
    start_date: datetime | None = None, end_date: datetime | None = None,
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    query = db.query(BmiRecord).filter(BmiRecord.user_id == user.id)
    if start_date:
        query = query.filter(BmiRecord.measured_at >= start_date)
    if end_date:
        query = query.filter(BmiRecord.measured_at <= end_date)
    return query.order_by(BmiRecord.measured_at.desc()).offset(skip).limit(limit).all()


@router.get("/latest", response_model=BmiRecordResponse | None)
def latest_record(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(BmiRecord).filter(BmiRecord.user_id == user.id).order_by(BmiRecord.measured_at.desc()).first()


@router.get("/compare")
def compare_records(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(BmiRecord).filter(BmiRecord.user_id == user.id).order_by(BmiRecord.measured_at.desc()).limit(2).all()
    if len(records) < 2:
        return {"available": False, "message": "At least two BMI records are required for comparison."}
    latest, previous = records
    return {
        "available": True,
        "latest": {"id": latest.id, "bmi": latest.bmi, "weight_kg": latest.weight_kg, "measured_at": latest.measured_at},
        "previous": {"id": previous.id, "bmi": previous.bmi, "weight_kg": previous.weight_kg, "measured_at": previous.measured_at},
        "bmi_change": round(latest.bmi - previous.bmi, 2),
        "weight_change_kg": round(latest.weight_kg - previous.weight_kg, 2),
    }


@router.get("/statistics")
def statistics(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(BmiRecord).filter(BmiRecord.user_id == user.id).order_by(BmiRecord.measured_at.asc()).all()
    if not records:
        return {"total_records": 0, "average_bmi": None, "min_bmi": None, "max_bmi": None, "bmi_trend": []}
    values = [record.bmi for record in records]
    return {
        "total_records": len(records),
        "average_bmi": round(sum(values) / len(values), 2),
        "min_bmi": min(values), "max_bmi": max(values),
        "latest_bmi": records[-1].bmi,
        "bmi_trend": [{"date": r.measured_at, "bmi": r.bmi, "weight_kg": r.weight_kg} for r in records]
    }


@router.patch("/records/{record_id}", response_model=BmiRecordResponse)
def update_record(record_id: int, payload: BmiUpdate, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    record = db.query(BmiRecord).filter(BmiRecord.id == record_id, BmiRecord.user_id == user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="BMI record not found")
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        if key in {"height_cm", "weight_kg", "measured_at"} and value is None:
            continue
        setattr(record, key, value)
    record.bmi = calculate_bmi(record.height_cm, record.weight_kg)
    record.category = classify_bmi(record.bmi)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(BmiRecord).filter(BmiRecord.id == record_id, BmiRecord.user_id == user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="BMI record not found")
    db.delete(record)
    db.commit()
    return None
