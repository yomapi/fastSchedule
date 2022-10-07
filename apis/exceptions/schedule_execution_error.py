class FailureExecutionError(Exception):
    """It occur when fail execute to run job"""

    @staticmethod
    def validate(return_code: int):
        if return_code > 0:
            raise FailureExecutionError("Schedule 실행 도중 에러가 발생하였습니다.")
