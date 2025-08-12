from typing import Dict, List

import pandas as pd


def read_excel_transactions(file_path: str) -> List[Dict]:
    """
    Считывает финансовые транзакции из файла Excel

    Args:
        file_path: Путь к Excel файлу (.xlsx)

    Returns:
        Список транзакций в формате словарей

    Raises:
        ValueError: Если файл имеет неверный формат
    """
    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path, engine="openpyxl")

        # Проверяем обязательные столбцы
        required_columns = ["id", "state", "date", "amount", "currency_code"]
        if not all(col in df.columns for col in required_columns):
            missing = set(required_columns) - set(df.columns)
            raise ValueError(f"Отсутствуют обязательные столбцы: {missing}")

        # Преобразуем в нужный формат
        transactions = []
        for _, row in df.iterrows():
            transaction = {
                "id": row["id"],
                "state": row["state"],
                "date": str(row["date"]),
                "operationAmount": {
                    "amount": float(row["amount"]),
                    "currency": {"name": row.get("currency_name", ""), "code": row["currency_code"]},
                },
                "description": row.get("description", ""),
                "from": row.get("from"),
                "to": row.get("to", ""),
            }
            transactions.append(transaction)

        return transactions

    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return []
