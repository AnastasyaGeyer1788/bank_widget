import json
import os
from typing import List, Dict, Union
from .logger_config import setup_logger  # Относительный импорт внутри пакета


# Инициализация логгера для модуля utils
logger = setup_logger('utils', 'utils.log')


def load_transactions_from_json(file_path: str) -> List[Dict[str, Union[str, int, float]]]:
    """Загружает данные о транзакциях из JSON-файла с логированием"""
    logger.debug(f"Начало загрузки файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций")
                return data

            logger.error("Файл не содержит список")
            return []

    except json.JSONDecodeError:
        logger.error("Ошибка декодирования JSON")
        return []
    except PermissionError:
        logger.error("Ошибка доступа к файлу")
        return []
    except Exception:
        logger.exception("Критическая ошибка при загрузке файла")
        return []
