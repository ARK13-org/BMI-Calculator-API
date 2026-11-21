from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    age: int | None = Field(default=None, ge=13, le=120)
    height_cm: float | None = Field(default=None, gt=50, le=280)


class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int | None
    height_cm: float | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
