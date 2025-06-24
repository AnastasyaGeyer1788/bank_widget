from src.widget import mask_account_card, get_date
from src.masks import get_mask_card_number, get_mask_account
from src.processing import sort_by_date, filter_by_state

if __name__ == "__main__":
    print(
        mask_account_card("Visa Platinum 7000792289606361")
    )  # Visa Platinum 7000 79** **** 6361
    print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305
    print(get_date("2024-03-11T02:26:18.671407"))  # Дата 11.03.2024

if __name__ == "__main__":
    # Пример данных для демонстрации
    demo_operations = [
        {"id": "41428829", "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": "939719570", "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": "594226727", "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    ]

    # Демонстрация фильтрации
    print("EXECUTED operations:")
    for op in filter_by_state(demo_operations):
        print(f"{op['date']} - {op['id']}")

    print("\nCANCELED operations:")
    for op in filter_by_state(demo_operations, "CANCELED"):
        print(f"{op['date']} - {op['id']}")

    # Демонстрация сортировки
    print("\nСортировка по убыванию (новые сначала):")
    for op in sort_by_date(demo_operations):
        print(f"{op['date']} - {op['id']}")

    print("\nСортировка по возрастанию (старые сначала):")
    for op in sort_by_date(demo_operations, reverse=False):
        print(f"{op['date']} - {op['id']}")

    # Комбинированный пример
    filtered = filter_by_state(demo_operations, "EXECUTED")
    sorted_ops = sort_by_date(filtered)
    print("\nВыполненные операции, отсортированные по дате:")
    for op in sorted_ops:
        print(f"{op['date']} - {op['id']}")

    # Тестирование mask_account_card
    test_cases = [
        "Visa Platinum 7000792289606361",
        "Maestro 1234567890123456",
        "Счет 73654108430135874305",
        "МИР 9876543210987654",
        "Счет 1234567890",
        "КартаБезПробелов1234567890",
        "Счет 123",
    ]

    for case in test_cases:
        print(f"Вход: {case}")
        print(f"Выход: {mask_account_card(case)}")
        print("-" * 50)

    # Тестирование get_date
    print(get_date("2024-03-11T02:26:18.671407"))
