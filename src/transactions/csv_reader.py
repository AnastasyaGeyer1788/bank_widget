from typing import Dict, List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict]:
    """Считывает финансовые транзакции из CSV-файла.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        List[Dict]: List of transactions as dictionaries.
    """
    df = pd.read_csv(file_path)
    return df.to_dict("records")
