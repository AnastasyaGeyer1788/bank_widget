from unittest.mock import mock_open, patch

import pytest

from src.transactions.csv_reader import read_csv_transactions

# Фикстура CSV


@pytest.fixture
def valid_csv_data():
    return """id;state;date;amount;currency_code;currency_name;description;from;to
1;EXECUTED;2023-01-01;100.0;USD;US Dollar;Payment;Card 1234;Account 5678
2;PENDING;2023-01-02;200.5;EUR;Euro;Transfer;;Account 9999
"""


# Фикстура с неполными данными


@pytest.fixture
def invalid_csv_data():
    return """id;state;date;amount;currency_code
1;EXECUTED;2023-01-01;;USD
2;PENDING;;200.5;EUR
"""


def test_read_valid_csv(valid_csv_data):
    """Тест чтения корректного CSV файла"""
    with patch("builtins.open", mock_open(read_data=valid_csv_data)):
        transactions = read_csv_transactions("dummy.csv")

        assert len(transactions) == 2
        assert transactions[0]["id"] == "1"
        assert transactions[0]["state"] == "EXECUTED"
        assert transactions[0]["operationAmount"]["amount"] == 100.0
        assert transactions[0]["operationAmount"]["currency"]["code"] == "USD"
        assert transactions[1]["description"] == "Transfer"


def test_read_invalid_csv(invalid_csv_data, capsys):
    """Тест чтения CSV с ошибками"""
    with patch("builtins.open", mock_open(read_data=invalid_csv_data)):
        transactions = read_csv_transactions("dummy.csv")

        assert len(transactions) == 0
        captured = capsys.readouterr()
        assert "пустая сумма" in captured.out
        assert "отсутствуют обязательные данные" in captured.out


def test_missing_required_fields():
    """Тест отсутствия обязательных полей"""
    csv_data = """date;amount;description
2023-01-01;100;Payment
"""
    with patch("builtins.open", mock_open(read_data=csv_data)):
        transactions = read_csv_transactions("dummy.csv")

        assert len(transactions) == 0


def test_file_not_found(capsys):
    """Тест обработки отсутствующего файла"""
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        transactions = read_csv_transactions("nonexistent.csv")

        assert len(transactions) == 0
        captured = capsys.readouterr()
        assert "Ошибка чтения CSV файла" in captured.out


def test_amount_conversion():
    """Тест преобразования суммы"""
    csv_data = """id;state;date;amount;currency_code;currency_name
1;EXECUTED;2023-01-01;100.50;USD;Dollar
2;EXECUTED;2023-01-02;invalid;EUR;Euro
"""
    with patch("builtins.open", mock_open(read_data=csv_data)):
        transactions = read_csv_transactions("dummy.csv")

        assert len(transactions) == 1
        assert transactions[0]["operationAmount"]["amount"] == 100.5


def test_empty_file():
    """Тест пустого файла"""
    with patch("builtins.open", mock_open(read_data="")):
        transactions = read_csv_transactions("empty.csv")

        assert len(transactions) == 0
