import logging
from functools import wraps
from typing import Any, Callable


def log(logger: logging.Logger = None):
    """Декоратор для логирования вызовов функций.

    Args:
        logger: Объект логгера. Если None, будет создан новый.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Используем переданный логгер или создаем новый
            func_logger = logger or logging.getLogger(func.__module__)

            try:
                func_logger.info(f"Вызов функции {func.__name__}")
                result = func(*args, **kwargs)
                func_logger.info(f"Функция {func.__name__} выполнена успешно")
                return result
            except Exception as e:
                func_logger.error(f"Ошибка в функции {func.__name__}: {str(e)}", exc_info=True)
                raise

        return wrapper

    return decorator
