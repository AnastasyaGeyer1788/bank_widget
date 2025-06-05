from src.widget import (
    mask_account_card,
)


def test_mask_account_card() -> None:
    """Тестирование функции маскировки карт и счетов."""
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"
