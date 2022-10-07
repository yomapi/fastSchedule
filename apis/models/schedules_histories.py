from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HistoryBase(BaseModel):
    schedule_id: Optional[int]
    dur_seconds: Optional[int] = Field(0, title="dur_seconds", ge=0)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class HistoryCreate(BaseModel):
    schedule_id: int = Field(title="schedule_id", ge=1)


class HistoryUpdate(BaseModel):
    dur_seconds: Optional[int] = Field(0, title="dur_seconds", ge=0)


class HistoryCreateReq(HistoryCreate):
    """create model"""


class HistoryCreateRes(BaseModel):
    schedule_history_id: int = Field(title="id", ge=1)


class HistoryUpdateReq(BaseModel):
    is_success: bool = Field(title="is_success")


class HistoryUpdateRes(HistoryCreateRes):
    """update model res"""


class HistoryUpdateRes(BaseModel):
    id: int = Field(title="id", ge=1)
    schedule_id: int = Field(title="schedule_id", ge=1)
    dur_seconds: int = Field(0, title="dur_seconds", ge=0)
    created_at: datetime
    updated_at: datetime
