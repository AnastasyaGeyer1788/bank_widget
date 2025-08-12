from src.logger_config import setup_logger

logger = setup_logger("masks", "masks.log")


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты."""
    logger.debug(f"Маскировка карты: {card_number}")
    try:
        card_str = str(card_number).replace(" ", "")
        if len(card_str) != 16 or not card_str.isdigit():
            raise ValueError("Номер карты должен содержать 16 цифр")
        return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    except Exception as e:
        logger.error(f"Ошибка маскировки карты: {e}")
        raise


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета."""
    logger.debug(f"Маскировка счета: {account_number}")
    try:
        account_str = str(account_number)
        if len(account_str) < 4 or not account_str.isdigit():
            raise ValueError("Номер счета должен содержать минимум 4 цифры")
        return f"**{account_str[-4:]}"
    except Exception as e:
        logger.error(f"Ошибка маскировки счета: {e}")
        raise
