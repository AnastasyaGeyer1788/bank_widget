import logging
from pathlib import Path
from typing import Optional


def setup_logger(
        module_name: str,
        log_file: str,
        log_level: int = logging.DEBUG,
        max_bytes: Optional[int] = 1024 * 1024,  # 1 MB
        backup_count: Optional[int] = 3
) -> logging.Logger:
    """Настройка отдельного логгера для каждого модуля с ротацией логов.

    Args:
        module_name: Имя модуля (например, 'utils' или 'masks')
        log_file: Имя файла для записи логов (например, 'utils.log')
        log_level: Уровень логирования (по умолчанию DEBUG)
        max_bytes: Максимальный размер файла перед ротацией
        backup_count: Количество сохраняемых резервных копий

    Returns:
        Настроенный объект логгера с файловым обработчиком
    """
    # Создаем папку logs в корне проекта
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True, mode=0o755)

    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    # Очищаем предыдущие обработчики
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    # Формат записи логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик с ротацией логов
    try:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            filename=str(logs_dir / log_file),
            mode='a',
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8',
            delay=False
        )
    except ImportError:
        file_handler = logging.FileHandler(
            filename=str(logs_dir / log_file),
            mode='a',
            encoding='utf-8'
        )

    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False

    return logger
