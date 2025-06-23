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
    """
    if not account_info:
        return account_info

    parts = account_info.rsplit(" ", 1)
    if len(parts) < 2:
        return account_info

    account_type, number = parts

    if not number.isdigit():
        return account_info

    if account_type.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        if len(number) < 16:
            return account_info
        masked_number = get_mask_card_number(number)

    return f"{account_type} {masked_number}"

def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_str: строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        Строка с датой в формате "ДД.ММ.ГГГГ"
    """
    date_part = date_str.split("T")[0]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"


if __name__ == "__main__":
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
