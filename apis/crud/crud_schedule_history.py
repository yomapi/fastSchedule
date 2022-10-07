import logging

from crud.crud_base import CRUDBase
from crud.crud_schedule import crud_schedule
from schemas.schedule import ScheduleHistory, Schedule
from models.schedules_histories import HistoryCreate, HistoryUpdate
from db.session import get_db_session


class CRUDHistory(CRUDBase[ScheduleHistory, HistoryCreate, HistoryUpdate]):
    def get_last_by_schedule_is_long_task(self, is_long_task: bool) -> ScheduleHistory:
        session = get_db_session()

        try:
            return (
                session.query(ScheduleHistory)
                .join(Schedule)
                .filter(
                    Schedule.schedule_type
                    == crud_schedule.get_schedule_type_by_is_long_task(is_long_task)
                )
                .order_by(ScheduleHistory.id.desc())
                .first()
            )
        except Exception as e:
            logging.error("failed to get last schedule by is long task:", e)
            raise e
        finally:
            session.close()


crud_schedule_history = CRUDHistory(ScheduleHistory)
