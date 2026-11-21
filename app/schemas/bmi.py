from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BmiCreate(BaseModel):
    height_cm: float = Field(gt=50, le=280)
    weight_kg: float = Field(gt=10, le=500)
    measured_at: datetime | None = None
    note: str | None = Field(default=None, max_length=1000)


class BmiUpdate(BaseModel):
    height_cm: float | None = Field(default=None, gt=50, le=280)
    weight_kg: float | None = Field(default=None, gt=10, le=500)
    measured_at: datetime | None = None
    note: str | None = Field(default=None, max_length=1000)


class BmiRecordResponse(BaseModel):
    id: int
    height_cm: float
    weight_kg: float
    bmi: float
    category: str
    note: str | None
    measured_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BmiCalculationResponse(BaseModel):
    bmi: float
    category: str
    healthy_weight_min_kg: float
    healthy_weight_max_kg: float
    message: str
