from datetime import datetime
from src.masks import mask_card_number, mask_account_number


def get_date(date_str: str) -> str:
    """Преобразует дату из формата ISO в формат DD.MM.YYYY"""
    try:
        date_obj = datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except (ValueError, IndexError, AttributeError):
        return date_str  # Возвращаем исходную строку при ошибке


def mask_account_card(data: str) -> str:
    """Маскирует номер карты или счета в зависимости от входных данных"""
    if not data or not isinstance(data, str):
        return data

    try:
        # Пробуем маскировку счета
        if "счет" in data.lower():
            parts = data.rsplit(' ', 1)
            if len(parts) == 2 and parts[1].isdigit():
                return f"{parts[0]} {mask_account_number(parts[1])}"

        # Пробуем маскировку карты
        parts = data.rsplit(' ', 1)
        if len(parts) == 2 and parts[1].isdigit():
            return f"{parts[0]} {mask_card_number(parts[1])}"

    except Exception:
        pass  # В случае любой ошибки возвращаем исходные данные

    return data
