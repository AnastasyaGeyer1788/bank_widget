from unittest.mock import patch
import pytest
from src.transactions.file_reader import read_transactions


def test_read_transactions_csv():
    with patch("src.transactions.file_reader.read_csv_transactions") as mock_csv:
        mock_csv.return_value = [{"amount": 100}]
        result = read_transactions("test.csv")
        assert result == [{"amount": 100}]


def test_read_transactions_excel():
    with patch("src.transactions.file_reader.read_excel_transactions") as mock_excel:
        mock_excel.return_value = [{"amount": 200}]
        result = read_transactions("test.xlsx")
        assert result == [{"amount": 200}]


def test_read_transactions_unsupported_format():
    with pytest.raises(ValueError):
        read_transactions("test.txt")
