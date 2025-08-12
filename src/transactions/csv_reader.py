import csv
from typing import Dict, List


def read_csv_transactions(file_path: str) -> List[Dict]:
    """Чтение CSV файла с обработкой пустых значений и ошибок"""
    transactions = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            # Проверка обязательных полей
            required_fields = {"id", "state", "date", "amount", "currency_code"}
            if not all(field in reader.fieldnames for field in required_fields):
                missing = required_fields - set(reader.fieldnames)
                print(f"Ошибка: отсутствуют обязательные поля: {missing}")
                return []

            for row_num, row in enumerate(reader, 1):
                try:
                    # Обработка пустого amount
                    amount_str = row.get("amount", "").strip()
                    if not amount_str:
                        print(f"Пропуск строки {row_num}: пустая сумма")
                        continue

                    # Преобразование в float с проверкой
                    try:
                        amount = float(amount_str)
                    except ValueError:
                        print(f"Пропуск строки {row_num}: неверный формат суммы '{amount_str}'")
                        continue

                    # Формирование транзакции
                    transaction = {
                        "id": row.get("id", "").strip(),
                        "state": row.get("state", "").strip().upper(),
                        "date": row.get("date", "").strip(),
                        "operationAmount": {
                            "amount": amount,
                            "currency": {
                                "name": row.get("currency_name", "").strip(),
                                "code": row.get("currency_code", "").strip(),
                            },
                        },
                        "description": row.get("description", "").strip(),
                        "from": row.get("from", "").strip(),
                        "to": row.get("to", "").strip(),
                    }

                    # Проверка обязательных полей
                    if not all([transaction["id"], transaction["state"], transaction["date"]]):
                        print(f"Пропуск строки {row_num}: отсутствуют обязательные данные")
                        continue

                    transactions.append(transaction)

                except Exception as e:
                    print(f"Ошибка в строке {row_num}: {str(e)}")
                    continue

        return transactions

    except Exception as e:
        print(f"Ошибка чтения CSV файла: {str(e)}")
        return []
