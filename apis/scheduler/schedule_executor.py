import subprocess
import os
from scheduler.constants import JOB_PATH
from exceptions.schedule_execution_error import FailureExecutionError


class ScheduleExecutor:
    def __init__(self, path_prefix=JOB_PATH):
        self.path_prefix = path_prefix

    def run(self, filename: str) -> None:
        file_path = f"{self.path_prefix}/{filename}"
        return_code = subprocess.call(["python", file_path])

        FailureExecutionError.validate(return_code)

    def get_list(self) -> tuple:
        text = os.popen(f"ls -al {self.path_prefix}").read()

        return tuple(
            filter(
                lambda x: x != "__init__.py",
                map(lambda x: x.split(" ")[-1], text.split("\n")[3:-1]),
            )
        )
