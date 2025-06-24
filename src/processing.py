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



