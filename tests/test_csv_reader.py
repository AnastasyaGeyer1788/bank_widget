from unittest.mock import patch, mock_open
import pandas as pd
from src.transactions.csv_reader import read_csv_transactions


def test_read_csv_transactions(mock_csv_data):
    """Тест чтения CSV: проверяет преобразование в список словарей."""
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame({
                'date': ['2023-01-01'],
                'amount': [100],
                'description': ['Payment']
            })

            result = read_csv_transactions("dummy.csv")

            assert isinstance(result, list), "Должен вернуться список"
            assert result[0]["amount"] == 100, "Неверная сумма транзакции"
