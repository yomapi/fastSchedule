from crud.crud_base import CRUDBase

from schemas.schedule import Schedule
from models.schedules import ScheduleCreate, ScheduleUpdate


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    pass


crud_schedule = CRUDSchedule(Schedule)
