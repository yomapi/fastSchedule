from crud.crud_base import CRUDBase

from schemas.schedule import Schedule
from models.schedules import ScheduleCreate, ScheduleUpdate
from enums.schedule_type import ScheduleType


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    def get_schedule_type_by_is_long_task(self, is_long_task: bool) -> str:
        return ScheduleType.LONG.value if is_long_task else ScheduleType.SHORT.value


crud_schedule = CRUDSchedule(Schedule)
