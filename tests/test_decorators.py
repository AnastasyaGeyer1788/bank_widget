from datetime import datetime

import pytest

from src.decorators import log


def test_log_to_file(tmp_path):
    """Тестирует логирование в файл при успешном выполнении и ошибке.

    Args:
        tmp_path: Фикстура pytest для создания временных файлов.

    Проверяет:
        - Запись в файл при успешном выполнении функции
        - Запись в файл при возникновении ошибки
        - Корректность формата логов (время, аргументы, результат)
    """
    filename = tmp_path / "test_log.txt"

    @log(filename=str(filename))
    def add(a, b):
        """Тестовая функция для сложения двух чисел."""
        return a + b

    # 1. Проверяем успешное выполнение
    add(2, 3)

    with open(filename, "r") as f:
        log_content = f.read()

    assert "add" in log_content
    assert "ok" in log_content
    assert "Args: (2, 3)" in log_content
    assert "Kwargs: {}" in log_content
    assert datetime.now().strftime("%Y-%m-%d") in log_content

    # 2. Проверяем логирование ошибки
    @log(filename=str(filename))
    def divide(a, b):
        """Тестовая функция для деления с возможной ошибкой."""
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with open(filename, "r") as f:
        log_content = f.read()

    assert "divide" in log_content
    assert "ZeroDivisionError" in log_content
    assert "Args: (1, 0)" in log_content
    assert "Kwargs: {}" in log_content


def test_log_to_console(capsys):
    """Тестирует вывод логов в консоль.

    Args:
        capsys: Фикстура pytest для перехвата вывода.

    Проверяет:
        - Вывод информации о вызове функции
        - Вывод информации об ошибках
    """

    @log()
    def multiply(a, b):
        """Тестовая функция для умножения двух чисел."""
        return a * b

    multiply(3, 4)
    captured = capsys.readouterr()
    console_output = captured.out

    assert "multiply" in console_output
    assert "ok" in console_output

    @log()
    def fail_func():
        """Тестовая функция, вызывающая исключение."""
        raise ValueError("Oops!")

    with pytest.raises(ValueError):
        fail_func()

    captured = capsys.readouterr()
    console_output = captured.out

    assert "fail_func" in console_output
    assert "ValueError" in console_output


def test_decorator_preserves_functionality():
    """Тестирует, что декоратор не нарушает работу функции.

    Проверяет:
        - Функция возвращает корректный результат
        - Декоратор не модифицирует поведение функции
    """

    @log()
    def subtract(a, b):
        """Тестовая функция для вычитания двух чисел."""
        return a - b

    assert subtract(5, 3) == 2


def test_log_with_args_and_kwargs(tmp_path):
    """Тестирует логирование функций с разными типами аргументов.

    Args:
        tmp_path: Фикстура pytest для создания временных файлов.

    Проверяет:
        - Логирование позиционных аргументов
        - Логирование именованных аргументов
        - Корректность формата логов
    """
    filename = tmp_path / "args_log.txt"

    @log(filename=str(filename))
    def greet(name, greeting="Hello"):
        """Тестовая функция с аргументами по умолчанию."""
        return f"{greeting}, {name}!"

    greet("Alice", greeting="Hi")

    with open(filename, "r") as f:
        log_content = f.read()

    assert "greet" in log_content
    assert "Args: ('Alice',)" in log_content
    assert "Kwargs: {'greeting': 'Hi'}" in log_content
    assert "greet ok" in log_content
