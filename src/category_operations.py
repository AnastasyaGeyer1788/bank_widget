from collections import Counter
from typing import Dict, List


def process_bank_operations(operations: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчет операций по категориям с использованием Counter.
    Сравнение производится без учета регистра.

    Args:
        operations: Список транзакций
        categories: Список категорий для анализа (регистр не важен)

    Returns:
        Словарь {категория: количество_операций}, включая все запрошенные категории

    Пример:
        >>> transactions = [
        ...     {'description': 'Перевод организации'},
        ...     {'description': 'Открытие вклада'},
        ...     {'description': 'Перевод с карты на карту'}
        ... ]
        >>> process_bank_operations(transactions, ['перевод', 'вклад'])
        {'перевод': 2, 'вклад': 1}
    """
    # Нормализуем категории к нижнему регистру для сравнения
    normalized_categories = [cat.lower() for cat in categories]
    category_counter = Counter()

    for op in operations:
        description = op.get("description", "").lower()
        # Находим все категории, которые встречаются в описании
        found_categories = [cat for cat in normalized_categories if cat in description]
        category_counter.update(found_categories)

    # Возвращаем результат с оригинальными названиями категорий
    return {categories[normalized_categories.index(cat)]: count for cat, count in category_counter.items()}
