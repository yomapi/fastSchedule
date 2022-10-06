from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from schemas.base import Base


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    subject = Column(String(50), nullable=False)
    comments = Column(String(100), nullable=True)
    schedule_type = Column(String(1), nullable=False)
    command = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False, unique=True)
    schedule_histories = relationship(
        "ScheduleHistory",
        back_populates="schedule",
    )


class ScheduleHistory(Base):
    __tablename__ = "schedule_history"

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey(Schedule.id))
    dur_seconds = Column(Integer, default=0)
    is_success = Column(Boolean, default=None)

    schedule = relationship("Schedule", back_populates="schedule_histories")
