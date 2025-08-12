from unittest.mock import patch

import pandas as pd
import pytest

from src.transactions.excel_reader import read_excel_transactions  # Укажите правильный путь импорта


@pytest.fixture
def mock_excel_data():
    """Фикстура с тестовыми данными Excel"""
    return {
        "id": [1, 2],
        "state": ["EXECUTED", "PENDING"],
        "date": ["2023-01-01", "2023-01-02"],
        "amount": [100.0, 200.5],
        "currency_code": ["USD", "EUR"],
        "currency_name": ["US Dollar", "Euro"],
        "description": ["Payment", "Transfer"],
        "from": ["Card 1234", None],
        "to": ["Account 5678", "Account 9999"],
    }


def test_successful_read(mock_excel_data):
    """Тест успешного чтения корректного Excel файла"""
    with patch("pandas.read_excel", return_value=pd.DataFrame(mock_excel_data)):
        transactions = read_excel_transactions("test.xlsx")
        assert len(transactions) == 2
        assert transactions[0]["id"] == 1
        assert transactions[0]["state"] == "EXECUTED"


def test_missing_required_columns():
    """Тест отсутствия обязательных столбцов"""
    test_data = {"id": [1], "date": ["2023-01-01"]}
    with patch("pandas.read_excel", return_value=pd.DataFrame(test_data)):
        transactions = read_excel_transactions("test.xlsx")
        assert transactions == []  # Ожидаем пустой список


def test_empty_file():
    """Тест пустого файла"""
    with patch("pandas.read_excel", return_value=pd.DataFrame()):
        transactions = read_excel_transactions("empty.xlsx")
        assert transactions == []


def test_invalid_amount_format():
    """Тест неверного формата суммы"""
    test_data = {
        "id": [1],
        "state": ["EXECUTED"],
        "date": ["2023-01-01"],
        "amount": ["invalid"],
        "currency_code": ["USD"],
    }
    with patch("pandas.read_excel", return_value=pd.DataFrame(test_data)):
        transactions = read_excel_transactions("invalid.xlsx")
        assert transactions == []  # Ожидаем пустой список


def test_file_not_found():
    """Тест отсутствия файла"""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        transactions = read_excel_transactions("nonexistent.xlsx")
        assert transactions == []  # Ожидаем пустой список


def test_partial_missing_data(mock_excel_data):
    """Тест частично отсутствующих данных"""
    # Удаляем некоторые необязательные поля
    del mock_excel_data["description"]
    del mock_excel_data["from"]

    with patch("pandas.read_excel", return_value=pd.DataFrame(mock_excel_data)):
        transactions = read_excel_transactions("partial.xlsx")

        assert len(transactions) == 2
        assert transactions[0]["description"] == ""
        assert transactions[1]["from"] is None
