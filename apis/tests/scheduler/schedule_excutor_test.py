from scheduler.schedule_executor import ScheduleExecutor

executor = ScheduleExecutor()


def test_run_schedule():
    executor.run("say_hello/main.py")
