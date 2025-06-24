from typing import Dict, List
from datetime import datetime


def filter_by_state(
    operations: List[Dict[str, str]],
    state: str = "EXECUTED"
) -> List[Dict[str, str]]:
    """Фильтрует список операций по указанному статусу.

    Args:
        operations: Список словарей с банковскими операциями.
        state: Статус для фильтрации (по умолчанию "EXECUTED").

    Returns:
        Отфильтрованный список операций с указанным статусом.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: List[Dict[str, str]],
    reverse: bool = True
) -> List[Dict[str, str]]:
    """Сортирует операции по дате.

    Args:
        operations: Список операций для сортировки.
        reverse: Если True - сортировка по убыванию (новые сначала),
                 если False - по возрастанию.

    Returns:
        Отсортированный список операций.
    """
    return sorted(
        operations,
        key=lambda x: datetime.fromisoformat(x["date"]),
        reverse=reverse
    )


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
