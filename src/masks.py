from logger_config import setup_logger


# Инициализация логгера для модуля masks
logger = setup_logger('masks', 'masks.log')


def mask_card_number(card_number: str) -> str:
    """Маскирует номер карты с логированием"""
    logger.debug(f"Начало маскировки карты: {card_number[:4]}...")

    try:
        if len(card_number) != 16 or not card_number.isdigit():
            error_msg = "Номер карты должен содержать 16 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info(f"Карта замаскирована: ...{card_number[-4:]}")
        return masked

    except Exception:
        logger.exception("Ошибка при маскировке карты")
        raise


def mask_account_number(account_number: str) -> str:
    """Маскирует номер счета с логированием"""
    logger.debug(f"Начало маскировки счета: ...{account_number[-4:]}")

    try:
        if len(account_number) < 4 or not account_number.isdigit():
            error_msg = "Номер счета должен содержать минимум 4 цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked = f"**{account_number[-4:]}"
        logger.info(f"Счет замаскирован: {masked}")
        return masked

    except Exception:
        logger.exception("Ошибка при маскировке счета")
        raise
