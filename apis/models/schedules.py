from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from croniter import croniter


subject_field = Field(title="subject", max_length=50)
comments_field = Field(None, title="comments", max_length=100)
type_field = Field(title="type", max_length=1)
command_field = Field(title="command", max_length=100)
file_name_field = Field(title="file_name", max_length=255)


class ScheduleBase(BaseModel):
    subject: Optional[str] = subject_field
    comments: Optional[str] = comments_field
    schedule_type: Optional[str] = type_field
    command: Optional[str] = command_field
    file_name: Optional[str] = file_name_field
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("command")
    def validate_cron_command(cls, v):
        if not croniter.is_valid(v):
            raise ValueError("invalid cron command")
        return v.title()


class ScheduleFindReq(BaseModel):
    limit: Optional[int] = Field(50, title="limit", ge=1)
    offset: Optional[int] = Field(0, title="offset", ge=0)
    order_by: Optional[str]
    file_name: Optional[str] = Field(title="file_name", max_length=255)
    schedule_type: Optional[str] = Field(title="schedule_type", max_length=1)


class ScheduleFindRes(BaseModel):
    count: int
    data: list


class ScheduleCreate(BaseModel):
    pass


class ScheduleUpdate(BaseModel):
    pass
