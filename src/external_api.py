import os
from typing import Dict, Union

import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env


def convert_transaction_amount(transaction: Dict[str, Union[str, float]]) -> float:
    """
    Конвертирует сумму транзакции в рубли (RUB).

    :param transaction: Словарь с данными о транзакции (должен содержать 'amount' и 'currency').
    :return: Сумма в рублях (float).
    """
    amount = transaction.get("amount", 0)
    currency = transaction.get("currency", "RUB").upper()

    if currency == "RUB":
        return float(amount)

    # Конвертация для USD/EUR
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError("API key not found in .env")

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        rate = data["rates"]["RUB"]
        return float(amount) * rate
    except (requests.RequestException, KeyError) as e:
        raise ValueError(f"Failed to convert currency: {e}")
