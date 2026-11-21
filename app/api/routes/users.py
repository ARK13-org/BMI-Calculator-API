from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserProfileUpdate, UserProfileResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile", response_model=UserProfileResponse)
def get_profile(user: User = Depends(get_current_user)):
    return user


@router.patch("/profile", response_model=UserProfileResponse)
def update_profile(payload: UserProfileUpdate, user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/account", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(user)
    db.commit()
    return None
