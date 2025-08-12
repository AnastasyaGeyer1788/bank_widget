from datetime import datetime
from typing import Dict, List


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрация по статусу с улучшенной обработкой данных"""
    if not operations:
        return []

    state = str(state).strip().upper()
    filtered_ops = []

    for op in operations:
        # Проверяем наличие и корректность поля state
        op_state = op.get("state")
        if not op_state or not isinstance(op_state, str):
            continue

        if op_state.strip().upper() == state:
            filtered_ops.append(op)

    return filtered_ops


def sort_by_date(operations: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """Сортирует операции по дате.

    Args:
        operations: Список операций для сортировки.
        reverse: Если True - сортировка по убыванию (новые сначала),
                 если False - по возрастанию.

    Returns:
        Отсортированный список операций.
    """
    return sorted(operations, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
