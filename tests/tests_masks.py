import pytest

from src.masks import get_mask_account, get_mask_card_number


# Фикстуры для тестирования функции get_mask_card_number
@pytest.fixture
def valid_card_number():
    return "1234567890123456"


@pytest.fixture
def short_card_number():
    return "1234567890"


@pytest.fixture
def long_card_number():
    return "12345678901234567890"


@pytest.fixture
def non_numeric_card_number():
    return "1234abcd56789012"


# Фикстуры для тестирования функции get_mask_account
@pytest.fixture
def valid_account_number():
    return "12345678"


@pytest.fixture
def short_account_number():
    return "123"


@pytest.fixture
def non_numeric_account_number():
    return "abcd1234"


# Тесты для функции get_mask_card_number
def test_get_mask_card_number_valid(valid_card_number):
    assert get_mask_card_number(valid_card_number) == "1234 56** **** 3456"


def test_get_mask_card_number_long(long_card_number):
    # Функция просто обрежет лишние цифры, так как берет срезы
    assert get_mask_card_number(long_card_number) == "1234 56** **** 7890"


def test_get_mask_card_number_non_numeric(non_numeric_card_number):
    # Функция должна работать с любыми строками, не только цифрами
    assert get_mask_card_number(non_numeric_card_number) == "1234 ab** **** 9012"


# Тесты для функции get_mask_account
def test_get_mask_account_valid(valid_account_number):
    assert get_mask_account(valid_account_number) == "**5678"


def test_get_mask_account_short(short_account_number):
    # Для коротких номеров вернет то, что есть
    assert get_mask_account(short_account_number) == "**123"


def test_get_mask_account_non_numeric(non_numeric_account_number):
    # Функция должна работать с любыми строками
    assert get_mask_account(non_numeric_account_number) == "**1234"


# Дополнительные тесты для граничных случаев
def test_get_mask_account_empty_string():
    assert get_mask_account("") == "**"
