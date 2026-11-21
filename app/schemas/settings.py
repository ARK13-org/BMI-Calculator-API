from pydantic import BaseModel, Field, ConfigDict


class SettingsUpdate(BaseModel):
    unit_system: str | None = Field(default=None, pattern="^(metric|imperial)$")
    notifications_enabled: bool | None = None
    theme: str | None = Field(default=None, pattern="^(light|dark|system)$")


class SettingsResponse(BaseModel):
    unit_system: str
    notifications_enabled: bool
    theme: str
    model_config = ConfigDict(from_attributes=True)
