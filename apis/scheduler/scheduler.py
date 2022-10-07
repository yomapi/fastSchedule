import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from croniter import croniter

from crud.crud_schedule import crud_schedule
from crud.crud_schedule_history import crud_schedule_history
from scheduler.schedule_executor import ScheduleExecutor
from exceptions.schedule_execution_error import FailureExecutionError
from schemas.schedule import Schedule, ScheduleHistory

DEFAULT_CHECK_MINUTES = 1
LONG_CHECK_MINUTES = 10
INTERVAL_TYPE = "interval"

schedule_executor = ScheduleExecutor()


class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler(
            {
                "apscheduler.jobstores.default": {
                    "type": "sqlalchemy",
                    "url": "sqlite:///jobs.sqlite",
                },
                "apscheduler.executors.default": {
                    "class": "apscheduler.executors.pool:ThreadPoolExecutor",
                    "max_workers": "2",
                },
                "apscheduler.executors.processpool": {
                    "type": "processpool",
                    "max_workers": "1",
                },
                "apscheduler.job_defaults.coalesce": "false",
                "apscheduler.job_defaults.max_instances": "1",
                "apscheduler.timezone": "Asia/Seoul",
            }
        )
        self.scheduler.start()

        try:
            self._init_jobs()
        except Exception as e:
            logging.error("occurred an error when initialize schedule jobs: ", e)
            logging.info("try to reinitialize schedule jobs")

            self._clean_all_jobs()
            self._init_jobs()

    def _init_jobs(self):
        self._clean_all_jobs()
        self.scheduler.add_job(
            TaskScheduler.run_default_task,
            INTERVAL_TYPE,
            minutes=DEFAULT_CHECK_MINUTES,
            id="default",
        )

        self.scheduler.add_job(
            TaskScheduler.run_long_running_task,
            INTERVAL_TYPE,
            minutes=LONG_CHECK_MINUTES,
            id="long_running",
        )

    @staticmethod
    def run_default_task():
        TaskScheduler.run_tasks_by_is_long_task(False, DEFAULT_CHECK_MINUTES)

    @staticmethod
    def run_long_running_task():
        TaskScheduler.run_tasks_by_is_long_task(True, LONG_CHECK_MINUTES)

    def _clean_all_jobs(self):
        self.scheduler.remove_job("default")
        self.scheduler.remove_job("long_running")

    # TODO: 동시 처리를 위해 좀더 strict하게 바꿀 것
    @staticmethod
    def is_execute_now(command: str, last_executed_time: datetime):
        end_time = datetime.now()
        iterator = croniter(command, end_time)
        prev_time = iterator.get_prev(datetime)
        return last_executed_time <= prev_time <= end_time

    @staticmethod
    def run_tasks_by_is_long_task(is_long_task: bool, check_minutes: int):
        last_history = crud_schedule_history.get_last_by_schedule_is_long_task(
            is_long_task
        )
        cur_time = datetime.now()
        last_executed_time = (
            last_history.created_at
            if last_history
            else cur_time - timedelta(minutes=check_minutes + 1)
        )
        target_schedules = TaskScheduler._extract_run_schedules(
            last_executed_time, is_long_task
        )

        for schedule in target_schedules:
            try:
                history = TaskScheduler.create_history(schedule)
                schedule_executor.run(schedule.file_name)
                TaskScheduler.end_history(history)
            except FailureExecutionError as e:
                TaskScheduler.end_history(history, False)

                logging.error(
                    f"failed to run schedule job."
                    f"schedule name: {schedule.subject}, filename: {schedule.file_name}"
                )
                logging.error(e)

    @staticmethod
    def create_history(schedule: Schedule) -> ScheduleHistory:
        return crud_schedule_history.create({"schedule_id": schedule.id})

    @staticmethod
    def end_history(
        history: ScheduleHistory, is_success: bool = True
    ) -> ScheduleHistory:
        params = {
            "is_success": is_success,
            "dur_seconds": (datetime.now() - history.updated_at).total_seconds(),
        }
        return crud_schedule_history.update(history.id, params)

    @staticmethod
    def _extract_run_schedules(
        last_executed_time: datetime, is_long_task: bool
    ) -> tuple:
        return tuple(
            filter(
                lambda x: TaskScheduler.is_execute_now(x.command, last_executed_time),
                crud_schedule.find(
                    {
                        "schedule_type": crud_schedule.get_schedule_type_by_is_long_task(
                            is_long_task
                        )
                    }
                ),
            )
        )
