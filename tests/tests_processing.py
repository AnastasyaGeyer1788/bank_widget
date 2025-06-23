import pytest
from datetime import datetime
from typing import Dict, List
from src.processing import filter_by_state, sort_by_date

# Фикстуры с тестовыми данными
@pytest.fixture
def sample_operations() -> List[Dict[str, str]]:
    return [
        {
            "id": "1",
            "state": "EXECUTED",
            "date": "2023-01-01T12:00:00.000000",
            "description": "Operation 1"
        },
        {
            "id": "2",
            "state": "PENDING",
            "date": "2023-01-02T12:00:00.000000",
            "description": "Operation 2"
        },
        {
            "id": "3",
            "state": "EXECUTED",
            "date": "2023-01-03T12:00:00.000000",
            "description": "Operation 3"
        },
        {
            "id": "4",
            "state": "CANCELED",
            "date": "2023-01-04T12:00:00.000000",
            "description": "Operation 4"
        },
        {
            "id": "5",
            "state": "EXECUTED",
            "date": "2023-01-05T12:00:00.000000",
            "description": "Operation 5"
        }
    ]

@pytest.fixture
def operations_without_state() -> List[Dict[str, str]]:
    return [
        {
            "id": "6",
            "date": "2023-01-06T12:00:00.000000",
            "description": "Operation 6"
        },
        {
            "id": "7",
            "date": "2023-01-07T12:00:00.000000",
            "description": "Operation 7"
        }
    ]

@pytest.fixture
def operations_with_invalid_dates() -> List[Dict[str, str]]:
    return [
        {
            "id": "8",
            "state": "EXECUTED",
            "date": "invalid-date",
            "description": "Operation 8"
        }
    ]

# Тесты для filter_by_state
def test_filter_by_state_executed(sample_operations):
    filtered = filter_by_state(sample_operations, "EXECUTED")
    assert len(filtered) == 3
    assert all(op["state"] == "EXECUTED" for op in filtered)

def test_filter_by_state_pending(sample_operations):
    filtered = filter_by_state(sample_operations, "PENDING")
    assert len(filtered) == 1
    assert filtered[0]["id"] == "2"

def test_filter_by_state_canceled(sample_operations):
    filtered = filter_by_state(sample_operations, "CANCELED")
    assert len(filtered) == 1
    assert filtered[0]["id"] == "4"

def test_filter_by_state_empty_list():
    assert filter_by_state([], "EXECUTED") == []

def test_filter_by_state_missing_state(operations_without_state):
    assert filter_by_state(operations_without_state, "EXECUTED") == []

# Тесты для sort_by_date
def test_sort_by_date_descending(sample_operations):
    sorted_ops = sort_by_date(sample_operations, reverse=True)
    dates = [op["date"] for op in sorted_ops]
    assert dates == [
        "2023-01-05T12:00:00.000000",
        "2023-01-04T12:00:00.000000",
        "2023-01-03T12:00:00.000000",
        "2023-01-02T12:00:00.000000",
        "2023-01-01T12:00:00.000000"
    ]

def test_sort_by_date_ascending(sample_operations):
    sorted_ops = sort_by_date(sample_operations, reverse=False)
    dates = [op["date"] for op in sorted_ops]
    assert dates == [
        "2023-01-01T12:00:00.000000",
        "2023-01-02T12:00:00.000000",
        "2023-01-03T12:00:00.000000",
        "2023-01-04T12:00:00.000000",
        "2023-01-05T12:00:00.000000"
    ]

def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []

def test_sort_by_date_invalid_date(operations_with_invalid_dates):
    with pytest.raises(ValueError):
        sort_by_date(operations_with_invalid_dates)

# Дополнительные тесты для edge cases
def test_sort_by_date_single_operation():
    single_op = [{
        "id": "9",
        "state": "EXECUTED",
        "date": "2023-01-09T12:00:00.000000",
        "description": "Single Operation"
    }]
    assert sort_by_date(single_op) == single_op

def test_filter_by_state_nonexistent_state(sample_operations):
    assert filter_by_state(sample_operations, "NONEXISTENT") == []
