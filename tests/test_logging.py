import json  # Добавлен импорт json
from pathlib import Path
from src.utils import load_transactions_from_json
from src.masks import mask_card_number, mask_account_number


def test_logging():
    """Тестирование системы логирования"""
    print("\n=== Тестирование системы логирования ===")

    # Тест успешных операций
    print("1. Тест успешных операций:")
    print(mask_card_number("1234567890123456"))  # Добавлен print для наглядности
    print(mask_account_number("12345678"))

    # Создаем тестовый JSON файл
    test_data = [{"id": 1, "amount": 100, "currency": "RUB"}]
    test_json = Path("test_operations.json")
    test_json.write_text(json.dumps(test_data), encoding="utf-8")
    loaded_data = load_transactions_from_json(str(test_json))
    print(f"Загружено: {loaded_data}")

    # Тест ошибок
    print("\n2. Тест ошибок:")
    try:
        mask_card_number("123")
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        mask_account_number("abc")
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    # Проверка файлов логов
    logs_dir = Path(__file__).parent.parent / "logs"
    print("\n3. Проверьте файлы логов:")
    for log_file in logs_dir.glob("*.log"):
        print(f"- {log_file} (размер: {log_file.stat().st_size} байт)")

    # Удаляем тестовый файл
    test_json.unlink(missing_ok=True)

if __name__ == "__main__":
    test_logging()
