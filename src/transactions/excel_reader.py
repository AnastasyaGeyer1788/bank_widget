from typing import Dict, List

import pandas as pd


def read_excel_transactions(file_path: str) -> List[Dict]:
    """Считывает финансовые транзакции из файла Excel.

    Args:
        file_path (str): Path to the Excel (.xlsx) file.

    Returns:
        List[Dict]: List of transactions as dictionaries.
    """
    df = pd.read_excel(file_path, engine="openpyxl")
    return df.to_dict("records")
