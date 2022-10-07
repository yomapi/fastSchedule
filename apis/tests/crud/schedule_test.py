import pytest
from crud.crud_schedule import crud_schedule


@pytest.mark.parametrize("is_long_task", [True, False])
def test_find_long_schedule(is_long_task):
    sut = crud_schedule.find(
        {"schedule_type": crud_schedule.get_schedule_type_by_is_long_task(is_long_task)}
    )
    assert isinstance(sut, list)
