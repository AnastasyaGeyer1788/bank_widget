import pytest

from src.widget import get_date, mask_account_card


# Фикстуры для функции mask_account_card
@pytest.fixture
def card_examples():
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ]


@pytest.fixture
def account_examples():
    return [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 1234567890123456", "счет **3456"),  # Проверка lowercase
        ("Счет 1234", "Счет **1234"),  # Проверка короткого номера
    ]


@pytest.fixture
def invalid_examples():
    return [
        "Просто строка без номера",
        "Слишком короткая Visa 123",
        "",  # Пустая строка
    ]


# Фикстуры для функции get_date
@pytest.fixture
def date_examples():
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
    ]


@pytest.fixture
def invalid_dates():
    return [
        "2024-03-11",  # Нет времени
        "11.03.2024",  # Уже в неправильном формате
        "invalid-date",
        "",
    ]


# Тесты для функции mask_account_card
def test_mask_account_card_cards(card_examples):
    for input_str, expected in card_examples:
        assert mask_account_card(input_str) == expected


def test_mask_account_card_accounts(account_examples):
    for input_str, expected in account_examples:
        assert mask_account_card(input_str) == expected


def test_mask_account_card_invalid(invalid_examples):
    for input_str in invalid_examples:
        # Проверяем, что функция возвращает строку без изменений
        assert mask_account_card(input_str) == input_str


# Тесты для функции get_date
def test_get_date_valid(date_examples):
    for input_str, expected in date_examples:
        assert get_date(input_str) == expected


# Дополнительные тесты для граничных случаев
def test_mask_account_card_mixed_case():
    assert mask_account_card("сЧет 12345678") == "сЧет **5678"
    assert mask_account_card("VIsa 1234567890123456") == "VIsa 1234 56** **** 3456"


def test_get_date_with_timezone():
    # Проверяем, что время и таймзона игнорируются
    assert get_date("2024-03-11T02:26:18+03:00") == "11.03.2024"
    assert get_date("2024-03-11T02:26:18Z") == "11.03.2024"
