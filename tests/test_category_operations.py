from typing import Dict, List

import pytest

from src.category_operations import process_bank_operations


@pytest.fixture
def sample_operations() -> List[Dict]:
    """Тестовые данные операций"""
    return [
        {"description": "Payment for groceries", "amount": 100},
        {"description": "Salary deposit", "amount": 1000},
        {"description": "Transfer to friend", "amount": 50},
        {"description": "Online payment", "amount": 75},
        {"description": "Cash withdrawal", "amount": 200},
    ]


def test_category_counting(sample_operations):
    """Тест подсчета операций по категориям"""
    categories = ["payment", "deposit", "transfer", "withdrawal"]
    result = process_bank_operations(sample_operations, categories)

    assert result == {
        "payment": 2,  # "Payment for groceries" и "Online payment"
        "deposit": 1,  # "Salary deposit"
        "transfer": 1,  # "Transfer to friend"
        "withdrawal": 1,  # "Cash withdrawal"
    }


def test_case_insensitive_categories(sample_operations):
    """Тест на регистронезависимость сравнения, но с сохранением оригинального регистра категорий"""
    categories = ["PAYMENT", "Deposit"]
    result = process_bank_operations(sample_operations, categories)

    # Проверяем что функция нашла операции независимо от регистра,
    # но сохранила оригинальный регистр в ключах результата
    assert "PAYMENT" in result
    assert result["PAYMENT"] == 2  # "Payment for groceries" и "Online payment"
    assert "Deposit" in result
    assert result["Deposit"] == 1  # "Salary deposit"


def test_no_matching_categories(sample_operations):
    """Тест, когда нет совпадений с категориями"""
    result = process_bank_operations(sample_operations, ["loan", "interest"])
    # Функция возвращает только категории с ненулевым счетом
    assert result == {}


def test_empty_categories_list(sample_operations):
    """Тест пустого списка категорий"""
    result = process_bank_operations(sample_operations, [])
    assert result == {}


def test_overlapping_categories(sample_operations):
    """Тест с пересекающимися категориями"""
    extended_ops = sample_operations + [{"description": "Payment transfer", "amount": 100}]
    result = process_bank_operations(extended_ops, ["payment", "transfer"])

    assert result == {
        "payment": 3,  # +1 новая операция "Payment transfer"
        "transfer": 2,  # +1 новая операция "Payment transfer"
    }
