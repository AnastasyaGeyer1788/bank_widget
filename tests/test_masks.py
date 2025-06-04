from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тестирование функции маскировки номера карты."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("9876543210987654") == "9876 54** **** 7654"
    assert get_mask_card_number("1111222233334444") == "1111 22** **** 4444"


def test_get_mask_account() -> None:
    """Тестирование функции маскировки номера счёта."""
    assert get_mask_account("73654108430135874305") == "**4305"
    assert get_mask_account("12345678901234567890") == "**7890"
    assert get_mask_account("987654321012345678") == "**5678"
    assert get_mask_account("11112222333344445555") == "**5555"


def test_mask_functions_with_short_input() -> None:
    """Тестирование обработки коротких входных данных."""
    # Для номера карты (минимальная длина 16 символов)
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

    # Для номера счёта (минимальная длина 4 символа)
    assert get_mask_account("1234") == "**1234"
    assert get_mask_account("1") == "**1"  # Крайний случай


def test_mask_functions_format() -> None:
    """Тестирование формата вывода."""
    card_mask = get_mask_card_number("7000792289606361")
    assert len(card_mask) == 19  # 16 цифр + 3 пробела
    assert card_mask.count("*") == 6
    assert card_mask.count(" ") == 3

    account_mask = get_mask_account("73654108430135874305")
    assert len(account_mask) == 6  # 2 звёздочки + 4 цифры
    assert account_mask.startswith("**")
    assert account_mask[2:].isdigit()
