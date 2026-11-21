from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_settings import UserSettings
from app.schemas.settings import SettingsUpdate, SettingsResponse

router = APIRouter(prefix="/settings", tags=["Settings"])


def ensure_settings(user: User, db: Session) -> UserSettings:
    settings = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    if settings is None:
        settings = UserSettings(user_id=user.id)
        db.add(settings); db.commit(); db.refresh(settings)
    return settings


@router.get("", response_model=SettingsResponse)
def get_settings(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ensure_settings(user, db)


@router.patch("", response_model=SettingsResponse)
def update_settings(payload: SettingsUpdate, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    settings = ensure_settings(user, db)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(settings, key, value)
    db.commit(); db.refresh(settings)
    return settings
