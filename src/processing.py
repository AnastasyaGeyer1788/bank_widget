from typing import List, Dict
from datetime import datetime


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует список операций по указанному статусу.
    """
    return [operation for operation in operations if operation.get("state") == state]

if __name__ == "__main__":
    # Пример из задания
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    ]

    print("EXECUTED operations:")
    print(filter_by_state(operations))

    print("\nCANCELED operations:")
    print(filter_by_state(operations, "CANCELED"))


def sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список операций по дате.
    """
    return sorted(
        operations,
        key=lambda x: datetime.fromisoformat(x["date"]),
        reverse=reverse
    )


if __name__ == "__main__":
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
    ]

    print("Сортировка по убыванию (новые сначала):")
    for op in sort_by_date(operations):
        print(f"{op['date']} - {op['id']}")

    print("\nСортировка по возрастанию (старые сначала):")
    for op in sort_by_date(operations, reverse=False):
        print(f"{op['date']} - {op['id']}")


filtered_ops = filter_by_state(operations, 'EXECUTED')
sorted_ops = sort_by_date(filtered_ops)
