import json
import os
from typing import Dict, List, Union


def load_transactions_from_json(file_path: str) -> List[Dict[str, Union[str, int, float]]]:
    """
    Загружает данные о транзакциях из JSON-файла.

    Args:
        file_path: Путь до JSON-файла с транзакциями.

    Returns:
        Список словарей с данными о транзакциях или пустой список, если файл не найден, пуст или содержит не список.
    """
    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            return []

    except (json.JSONDecodeError, PermissionError, UnicodeDecodeError):
        return []
