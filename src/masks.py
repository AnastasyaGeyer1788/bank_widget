def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX.

    :param card_number: Номер карты (16 цифр)
    :return: Маскированный номер карты
    """
    card_str = str(card_number)
    masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате **XXXX.

    :param account_number: Номер счета
    :return: Маскированный номер счета
    """
    account_str = str(account_number)
    masked_account = f"**{account_str[-4:]}"
    return masked_account

