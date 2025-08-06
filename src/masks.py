from logger_config import setup_logger

logger = setup_logger("masks", "masks.log")


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX.

    Args:
        card_number: Номер карты (16 цифр)

    Returns:
        Маскированный номер карты

    Examples:
        >>> get_mask_card_number("1234567890123456")
        '1234 56** **** 3456'
    """
    logger.debug(f"Начало маскировки номера карты: {card_number}")

    try:
        card_str = str(card_number)
        if len(card_str) != 16 or not card_str.isdigit():
            error_msg = f"Неверный формат номера карты: {card_number}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        logger.info(f"Успешная маскировка карты: {card_number} -> {masked_number}")
        return masked_number

    except Exception as e:
        logger.exception(f"Ошибка при маскировке карты: {str(e)}")
        raise


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX.

    Args:
        account_number: Номер счета

    Returns:
        Маскированный номер счета

    Examples:
        >>> get_mask_account("12345678")
        '**5678'
    """
    logger.debug(f"Начало маскировки номера счета: {account_number}")

    try:
        account_str = str(account_number)
        if len(account_str) < 4 or not account_str.isdigit():
            error_msg = f"Неверный формат номера счета: {account_number}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked_account = f"**{account_str[-4:]}"
        logger.info(f"Успешная маскировка счета: {account_number} -> {masked_account}")
        return masked_account

    except Exception as e:
        logger.exception(f"Ошибка при маскировке счета: {str(e)}")
        raise
