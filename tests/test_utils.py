import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions_from_json


def test_load_transactions_from_json_valid_file():
    """Тест загрузки корректного JSON-файла со списком транзакций."""
    test_data = [{"id": 1, "amount": 100, "currency": "RUB"}, {"id": 2, "amount": 50, "currency": "USD"}]

    mock_file = mock_open(read_data=json.dumps(test_data))
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("dummy_path.json")

    assert result == test_data


def test_load_transactions_from_json_empty_list():
    """Тест загрузки файла с пустым списком."""
    mock_file = mock_open(read_data=json.dumps([]))
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("dummy_path.json")

    assert result == []


def test_load_transactions_from_json_invalid_content():
    """Тест загрузки файла с не-списком (должен вернуть пустой список)."""
    mock_file = mock_open(read_data=json.dumps({"not": "a list"}))
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("dummy_path.json")

    assert result == []


def test_load_transactions_from_json_nonexistent_file():
    """Тест обработки несуществующего файла."""
    with patch("os.path.exists", return_value=False):
        result = load_transactions_from_json("non_existent_file.json")
    assert result == []


def test_load_transactions_from_json_invalid_json():
    """Тест обработки битого JSON-файла."""
    mock_file = mock_open(read_data="{invalid json}")
    mock_file.side_effect = json.JSONDecodeError("Expecting value", "", 0)
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("dummy_path.json")

    assert result == []


def test_load_transactions_from_json_permission_error():
    """Тест обработки ошибки доступа к файлу."""
    with patch("builtins.open", side_effect=PermissionError("No access")), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("restricted_file.json")
    assert result == []


def test_load_transactions_from_json_empty_file():
    """Тест обработки пустого файла."""
    mock_file = mock_open(read_data="")
    mock_file.side_effect = json.JSONDecodeError("Expecting value", "", 0)
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("dummy_path.json")

    assert result == []
