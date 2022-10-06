from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from crud.crud_schedule import crud_schedule
from schemas.schedule import Schedule
from models.schedules import ScheduleFindReq, ScheduleFindRes
from models.except_msg import ExceptMessage

router = APIRouter()
schedule_sort_option = {
    "ASC_ID": Schedule.id.asc(),
    "DESC_ID": Schedule.id.desc(),
    "ASC_SUBJECT": Schedule.subject.asc(),
    "DESC_SUBJECT": Schedule.subject.desc(),
    "ASC_TYPE": Schedule.schedule_type.asc(),
    "DESC_TYPE": Schedule.schedule_type.desc(),
    "ASC_COMMENTS": Schedule.comments.asc(),
    "DESC_COMMENTS": Schedule.comments.desc(),
    "ASC_COMMANDS": Schedule.command.asc(),
    "DESC_COMMANDS": Schedule.command.desc(),
}


def _validate_schedule_order_by(order_by):
    return order_by is None or order_by in schedule_sort_option.keys()


def _get_queries(params):
    return {
        key: value
        for (key, value) in params.items()
        if key not in ["limit", "offset", "order_by"]
    }


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ScheduleFindRes,
    responses={
        400: {"model": ExceptMessage},
    },
)
async def find(params: ScheduleFindReq = Depends()):
    options = params.dict()

    is_valid = _validate_schedule_order_by(options["order_by"])
    if not is_valid:
        raise ValueError("올바른 정렬값이 아닙니다.")
    order_by = (
        options["order_by"]
        if options["order_by"] is None
        else schedule_sort_option.get(options["order_by"])
    )
    parsed_queries = _get_queries(options)
    schedules = crud_schedule.find(
        queries=parsed_queries,
        order_by=order_by,
        limit=options["limit"],
        offset=options["offset"],
    )
    data = ScheduleFindRes(count=len(schedules), data=schedules)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
