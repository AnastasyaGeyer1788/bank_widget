import logging
from pathlib import Path


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """Настройка logger для модуля.

    Args:
        name: Имя logger
        log_file: Имя файла для логов
        level: Уровень логирования

    Returns:
        Настроенный объект logger
    """
    # Создаем папку logs если ее нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Создаем logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Форматер
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Обработчик файла (перезаписывает файл при каждом запуске)
    file_handler = logging.FileHandler(filename=logs_dir / log_file, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Добавляем обработчик к logger
    logger.addHandler(file_handler)

    return logger
