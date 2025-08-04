import json
import os
from typing import Dict, List, Union

from logger_config import setup_logger

logger = setup_logger('utils', 'utils.log')


def load_transactions_from_json(file_path: str) -> List[Dict[str, Union[str, int, float]]]:
    """Загружает данные о транзакциях из JSON-файла.

    Args:
        file_path: Путь до JSON-файла с транзакциями.

    Returns:
        Список словарей с данными о транзакциях или пустой список, если файл не найден, пуст или содержит не список.
    """
    logger.debug(f"Начало загрузки данных из файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
                return data

            logger.warning(f"Файл {file_path} не содержит список (получен тип {type(data)})")
            return []

    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}")
        return []
    except PermissionError:
        logger.error(f"Ошибка доступа к файлу {file_path}")
        return []
    except UnicodeDecodeError:
        logger.error(f"Ошибка кодировки файла {file_path}")
        return []
    except Exception:
        logger.exception(f"Неожиданная ошибка при обработке файла {file_path}")
        return []
