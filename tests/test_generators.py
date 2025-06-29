import pytest
from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


# Фикстуры с тестовыми данными
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "operationAmount": {"currency": {"code": "EUR"}},
            "description": "Перевод со счета на счет",
        },
    ]


# Тесты для filter_by_currency
def test_filter_by_currency_usd(sample_transactions):
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["id"] == 939719570


def test_filter_by_currency_empty_result(sample_transactions):
    assert len(list(filter_by_currency(sample_transactions, "JPY"))) == 0


# Тесты для transaction_descriptions
def test_transaction_descriptions_basic(sample_transactions):
    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions == ["Перевод организации", "Перевод со счета на счет"]


# Тесты для card_number_generator
@pytest.mark.parametrize(
    "start,end,expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (
            9999,
            10001,
            ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"],
        ),
    ],
)
def test_card_number_generator_valid_ranges(start, end, expected):
    assert list(card_number_generator(start, end)) == expected


def test_card_number_generator_format():
    card_number = next(card_number_generator(1234567812345678, 1234567812345678))
    assert card_number == "1234 5678 1234 5678"


def test_card_number_generator_invalid_ranges():
    with pytest.raises(ValueError):
        list(card_number_generator(0, 1))  # start < 1

    with pytest.raises(ValueError):
        list(card_number_generator(2, 1))  # start > end

    with pytest.raises(ValueError):
        list(card_number_generator(9999999999999999, 10000000000000000))  # end > max


def test_card_number_generator_large_range():
    """Тест генерации большого диапазона без проверки всех значений"""
    gen = card_number_generator(1, 1000)
    first = next(gen)
    last = None
    for last in gen:  # Пропускаем промежуточные значения
        pass
    assert first == "0000 0000 0000 0001"
    assert last == "0000 0000 0000 1000"
