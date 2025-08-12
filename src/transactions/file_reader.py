import json
from pathlib import Path
from typing import Dict, List, Union


def read_transactions(file_path: Union[str, Path]) -> List[Dict]:
    """
    Считывает транзакции из файлов JSON, CSV или Excel

    Args:
        file_path: Путь к файлу (поддерживаются .json, .csv, .xlsx)

    Returns:
        Список транзакций в формате словарей

    Raises:
        ValueError: Если формат файла не поддерживается
        FileNotFoundError: Если файл не существует
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path

    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == ".json":
        return _read_json_file(file_path)
    elif suffix == ".csv":
        from .csv_reader import read_csv_transactions

        return read_csv_transactions(str(file_path))
    elif suffix == ".xlsx":
        from .excel_reader import read_excel_transactions

        return read_excel_transactions(str(file_path))
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {suffix}")


def _read_json_file(file_path: Path) -> List[Dict]:
    """Чтение и обработка JSON файла с транзакциями"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Если JSON представляет собой список транзакций
            if isinstance(data, list):
                return data
            # Если JSON имеет структуру {"transactions": [...]}
            elif isinstance(data, dict) and "transactions" in data:
                return data["transactions"]
            else:
                raise ValueError("Неверная структура JSON файла")

    except json.JSONDecodeError:
        raise ValueError("Ошибка декодирования JSON")
    except Exception as e:
        raise ValueError(f"Ошибка чтения JSON файла: {str(e)}")
