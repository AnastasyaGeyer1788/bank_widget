import logging
from io import StringIO

import pytest

from src.decorators import log


@pytest.fixture
def setup_logger():
    """Фикстура для настройки логгера с выводом в StringIO"""
    log_stream = StringIO()
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    logger.addHandler(handler)

    return logger, log_stream


def test_log_successful_execution(setup_logger):
    """Тест логирования успешного выполнения функции"""
    logger, log_stream = setup_logger

    @log(logger=logger)
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5

    log_content = log_stream.getvalue()
    assert "INFO:Вызов функции add" in log_content
    assert "INFO:Функция add выполнена успешно" in log_content


def test_log_failed_execution(setup_logger):
    """Тест логирования ошибки в функции"""
    logger, log_stream = setup_logger

    @log(logger=logger)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    log_content = log_stream.getvalue()
    assert "INFO:Вызов функции divide" in log_content
    assert "ERROR:Ошибка в функции divide: division by zero" in log_content


def test_log_with_default_logger():
    log_stream = StringIO()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(log_stream))

    @log()
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)
    assert result == 12

    log_content = log_stream.getvalue()
    assert "Вызов функции multiply" in log_content
    assert "Функция multiply выполнена успешно" in log_content

    # Очищаем обработчики
    logger.handlers.clear()


def test_log_preserves_metadata():
    """Тест сохранения метаданных функции"""

    @log()
    def original_func():
        """Тестовая функция"""
        pass

    assert original_func.__name__ == "original_func"
    assert original_func.__doc__ == "Тестовая функция"


def test_log_with_args_and_kwargs(setup_logger):
    """Тест логирования функций с аргументами"""
    logger, log_stream = setup_logger

    @log(logger=logger)
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}"

    greet("Alice", greeting="Hi")

    log_content = log_stream.getvalue()
    assert "INFO:Вызов функции greet" in log_content
    assert "INFO:Функция greet выполнена успешно" in log_content
