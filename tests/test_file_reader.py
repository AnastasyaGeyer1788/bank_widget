from unittest.mock import patch

import pytest

from src.transactions.file_reader import read_transactions


def test_read_transactions_csv():
    """Тест чтения CSV файла с проверкой существования файла"""
    with patch("pathlib.Path.exists", return_value=True), patch(
        "src.transactions.csv_reader.read_csv_transactions"
    ) as mock_csv:

        mock_csv.return_value = [{"amount": 100}]
        result = read_transactions("test.csv")

        assert result == [{"amount": 100}]
        mock_csv.assert_called_once_with("test.csv")


def test_read_transactions_excel():
    """Тест чтения Excel файла с проверкой существования файла"""
    with patch("pathlib.Path.exists", return_value=True), patch(
        "src.transactions.excel_reader.read_excel_transactions"
    ) as mock_excel:

        mock_excel.return_value = [{"amount": 200}]
        result = read_transactions("test.xlsx")

        assert result == [{"amount": 200}]
        mock_excel.assert_called_once_with("test.xlsx")


def test_read_transactions_unsupported_format(tmp_path):
    """Тест неподдерживаемого формата файла"""
    file_path = tmp_path / "test.txt"
    file_path.touch()  # Создаем реальный файл для теста

    with pytest.raises(ValueError, match="Неподдерживаемый формат файла"):
        read_transactions(file_path)


def test_read_nonexistent_file():
    """Тест обработки отсутствующего файла"""
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            read_transactions("nonexistent.csv")
