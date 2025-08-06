from typing import Dict, List

from .csv_reader import read_csv_transactions
from .excel_reader import read_excel_transactions


def read_transactions(file_path: str) -> List[Dict]:
    """Считывает транзакции из файлов CSV или Excel.

    Args:
        file_path (str): Path to the file.

    Returns:
        List[Dict]: List of transactions.

    Raises:
        ValueError: If file format is unsupported.
    """
    if file_path.endswith(".csv"):
        return read_csv_transactions(file_path)
    elif file_path.endswith(".xlsx"):
        return read_excel_transactions(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and XLSX are allowed.")
