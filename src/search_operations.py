import re
from typing import Dict, List


def process_bank_search(data: List[Dict], search_data: str) -> List[Dict]:
    """Ищет операции в описании которых есть заданная для поиска строка.

    Args:
        data: Список словарей с операциями
        search_data: Строка для поиска в описании операций

    Returns:
        Список операций, содержащих search_data в описании
    """
    if not search_data or not data:
        return []

    result = []

    for operation in data:
        try:
            description = operation.get("description", "")
            if re.search(search_data, description, flags=re.IGNORECASE):
                result.append(operation)
        except (TypeError, re.error):
            continue

    return result
