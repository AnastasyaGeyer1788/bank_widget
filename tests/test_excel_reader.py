from unittest.mock import patch
from src.transactions.excel_reader import read_excel_transactions


def test_read_excel_transactions(mock_excel_data):
    """Тест чтения Excel: проверяет вызов pd.read_excel и формат результата."""
    with patch("pandas.read_excel", return_value=mock_excel_data) as mock_read_excel:
        result = read_excel_transactions("dummy.xlsx")

        mock_read_excel.assert_called_once_with("dummy.xlsx", engine='openpyxl')
        assert result[0]["amount"] == 200, "Сумма должна быть 200"
