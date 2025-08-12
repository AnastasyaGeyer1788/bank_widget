from datetime import datetime

from src.masks import (
    get_mask_account,
    get_mask_card_number,
)


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в строке формата "Тип Номер".
    Возвращает строку без изменений, если не удалось определить тип и номер.

    Args:
        account_info: строка формата "Visa Platinum 7000792289606361" или
                     "Счет 73654108430135874305"

    Returns:
        Строку с замаскированным номером или исходную строку, если формат неверный

    Примеры:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
        >>> mask_account_card("Неверный формат")
        'Неверный формат'
    """
    if not account_info or not isinstance(account_info, str):
        return account_info

    try:
        parts = account_info.rsplit(" ", 1)
        if len(parts) != 2:
            return account_info

        account_type, number = parts
        number = number.strip()

        if not number.isdigit():
            return account_info

        if account_type.lower() == "счет":
            masked_number = get_mask_account(number)
        else:
            # Проверяем, что номер карты содержит 16 цифр
            if len(number) != 16:
                return account_info
            masked_number = get_mask_card_number(number)

        return f"{account_type} {masked_number}"

    except Exception:
        # В случае любой ошибки возвращаем исходную строку
        return account_info


def get_date(date_str: str) -> str:
    """
    Преобразует дату из различных форматов в формат ДД.ММ.ГГГГ.

    Args:
        date_str: строка с датой (может быть в формате ISO, "YYYY-MM-DD",
                 "YYYY-MM-DD HH:MM:SS" и др.)

    Returns:
        Строка с датой в формате "ДД.ММ.ГГГГ" или исходная строка при ошибке.

    Примеры:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
        >>> get_date("2024-03-11T02:26:18+03:00")
        '11.03.2024'
        >>> get_date("2024-03-11Z")
        '11.03.2024'
    """
    if not date_str or not isinstance(date_str, str):
        return "Дата не указана"

    try:
        # Удаляем всё после знака '+' или 'Z' (часовой пояс)
        date_without_tz = date_str.split("+")[0].split("Z")[0]

        # Удаляем микросекунды, если они есть
        cleaned_date = date_without_tz.split(".")[0]

        # Пробуем разные форматы дат (добавлен %z для поясов, но он не обязателен)
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(cleaned_date, fmt)
                return dt.strftime("%d.%m.%Y")
            except ValueError:
                continue

        return date_str  # Если формат не распознан
    except Exception:
        return "Некорректная дата"
