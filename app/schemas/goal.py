from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class GoalCreate(BaseModel):
    title: str = Field(default="Weight goal", min_length=2, max_length=120)
    target_weight_kg: float = Field(gt=10, le=500)
    target_date: datetime | None = None


class GoalUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=120)
    target_weight_kg: float | None = Field(default=None, gt=10, le=500)
    target_date: datetime | None = None
    is_active: bool | None = None


class GoalResponse(BaseModel):
    id: int
    title: str
    target_weight_kg: float
    target_date: datetime | None
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
