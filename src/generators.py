from typing import Iterator, Dict, Any


def filter_by_currency(
    transactions: Iterator[Dict[str, Any]], currency_code: str
) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по коду валюты.

    :param transactions: итератор словарей с транзакциями
    :param currency_code: код валюты для фильтрации (например, "USD")
    :yield: транзакции, где валюта операции соответствует заданной
    """
    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == currency_code:
                yield transaction
        except (KeyError, TypeError):
            continue


def transaction_descriptions(transactions: Iterator[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описания транзакций по очереди.

    :param transactions: итератор словарей с транзакциями
    :yield: описание транзакции (строка)
    """
    for transaction in transactions:
        yield transaction.get(
            "description", ""
        )  # Возвращаем пустую строку, если описания нет


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в заданном диапазоне

    :param start: начальный номер (от 1)
    :param stop: конечный номер (до 9999999999999999)
    :yield: номер карты в формате XXXX XXXX XXXX XXXX
    :raises ValueError: если диапазон некорректен
    """
    if start < 1 or stop > 9999999999999999:
        raise ValueError("Номер карты должен быть в диапазоне от 1 до 9999999999999999")
    if start > stop:
        raise ValueError("Начальное значение должно быть меньше или равно конечному")

    for number in range(start, stop + 1):
        card_num = f"{number:016d}"
        yield f"{card_num[:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"

