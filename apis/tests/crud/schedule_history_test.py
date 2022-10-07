import pytest
from crud.crud_schedule_history import crud_schedule_history


def test_create_schedule_history():
    sut = crud_schedule_history.create({"schedule_id": 0})
    assert sut == None
