import json
import pytest
from unittest.mock import mock_open, patch
from src.utils import load_transactions_from_json


# Фикстурные данные
@pytest.fixture
def valid_transactions():
    return [{"id": 1, "amount": 100, "currency": "RUB"},
            {"id": 2, "amount": 50, "currency": "USD"}]


def test_load_valid_json_file(valid_transactions):
    """Тест загрузки корректного JSON-файла со списком транзакций"""
    mock_file = mock_open(read_data=json.dumps(valid_transactions))
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("test.json")
    assert result == valid_transactions


def test_load_empty_list():
    """Тест загрузки файла с пустым списком"""
    mock_file = mock_open(read_data=json.dumps([]))
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("test.json")
    assert result == []


def test_load_non_list_content():
    """Тест загрузки файла с не-списком"""
    mock_file = mock_open(read_data=json.dumps({"key": "value"}))
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("test.json")
    assert result == []


def test_file_not_found():
    """Тест обработки несуществующего файла"""
    with patch("os.path.exists", return_value=False):
        result = load_transactions_from_json("missing.json")
    assert result == []


def test_invalid_json_format():
    """Тест обработки битого JSON"""
    m = mock_open(read_data="{invalid}")
    m.side_effect = json.JSONDecodeError("Error", "doc", 1)
    with patch("builtins.open", m), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("broken.json")
    assert result == []


def test_permission_denied():
    """Тест обработки ошибки доступа"""
    with patch("builtins.open", side_effect=PermissionError), \
            patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("restricted.json")
    assert result == []


def test_empty_file():
    """Тест обработки полностью пустого файла"""
    m = mock_open(read_data="")
    m.side_effect = json.JSONDecodeError("Error", "doc", 1)
    with patch("builtins.open", m), patch("os.path.exists", return_value=True):
        result = load_transactions_from_json("empty.json")
    assert result == []


def test_real_file_loading():
    """Интеграционный тест с реальным файлом (опциональный)"""
    try:
        result = load_transactions_from_json("data/operations.json")
        assert isinstance(result, list)
        print(f"\nЗагружено транзакций: {len(result)}")
    except FileNotFoundError:
        pytest.skip("Тестовый файл не найден")
