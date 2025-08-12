from pathlib import Path
from typing import Any, Dict, List

from src.external_api import convert_transaction_amount
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.search_operations import process_bank_search
from src.transactions.file_reader import read_transactions
from src.widget import get_date, mask_account_card


def print_transaction(transaction: Dict[str, Any]) -> None:
    """Форматированный вывод транзакции в точном соответствии с требованиями"""
    try:
        # Дата в формате ДД.ММ.ГГГГ
        date = get_date(transaction.get("date", ""))

        # Описание операции
        description = transaction.get("description", "")

        # Маскировка реквизитов
        from_info = mask_account_card(str(transaction.get("from", ""))) if transaction.get("from") else None
        to_info = mask_account_card(str(transaction.get("to", "")))

        # Получение суммы и валюты
        amount_info = transaction.get("operationAmount", {})
        amount = amount_info.get("amount", 0)
        currency = amount_info.get("currency", {}).get("code", "RUB")

        # Вывод транзакции
        print(f"{date} {description}")

        if from_info:
            print(f"{from_info} -> {to_info}")
        else:
            print(to_info)

        # Форматирование суммы
        if currency != "RUB":
            converted = convert_transaction_amount(transaction)
            amount_rub = converted["operationAmount"]["amount"]
            print(f"Сумма: {amount} {currency} (~{amount_rub} руб.)")
        else:
            print(f"Сумма: {amount} руб.")

        print()  # Пустая строка между транзакциями

    except Exception as e:
        print(f"\nОшибка при выводе транзакции: {e}")
        print("Сырые данные:", transaction)


def get_user_choice(prompt: str, options: List[str]) -> str:
    """Получение выбора пользователя с валидацией"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print(f"Ошибка: допустимые варианты - {', '.join(options)}")


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор файла
    file_choice = get_user_choice("Ваш выбор (1-3): ", ["1", "2", "3"])
    file_map = {"1": "operations.json", "2": "transactions.csv", "3": "transactions_excel.xlsx"}
    file_path = Path("data") / file_map[file_choice]
    print(f"\nДля обработки выбран {file_map[file_choice].split('.')[-1].upper()}-файл.")

    # Загрузка данных
    transactions = read_transactions(file_path)

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        status = input("Ваш выбор: ").strip().upper()

        if status in valid_statuses:
            transactions = filter_by_state(transactions, status)
            print(f"\nОперации отфильтрованы по статусу '{status}'")
            break
        print(f"\nСтатус операции '{status}' недоступен.")

    # Дополнительные фильтры
    if get_user_choice("\nОтсортировать операции по дате? (да/нет): ", ["да", "нет"]) == "да":
        order = get_user_choice("Отсортировать по возрастанию или по убыванию? ", ["возрастанию", "убыванию"])
        transactions = sort_by_date(transactions, reverse=order == "убыванию")

    if get_user_choice("\nВыводить только рублевые транзакции? (да/нет): ", ["да", "нет"]) == "да":
        transactions = list(filter_by_currency(transactions, "RUB"))

    if get_user_choice("\nОтфильтровать по ключевому слову в описании? (да/нет): ", ["да", "нет"]) == "да":
        keyword = input("Введите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, keyword)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}\n")
        for tx in transactions:
            print_transaction(tx)


if __name__ == "__main__":
    main()
