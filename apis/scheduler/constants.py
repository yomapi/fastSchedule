import os
from pathlib import Path

CRON_COMMAND_REGEX = r"(@(annually|yearly|monthly|weekly|daily|hourly|reboot))|(@every (\d+(ns|us|µs|ms|s|m|h))+)|((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})"
JOB_PATH = f"{Path(os.path.dirname(__file__)).resolve().parents[1]}/schedules/cmd"
