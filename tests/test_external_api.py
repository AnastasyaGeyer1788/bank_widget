import unittest
from unittest.mock import Mock, patch

import requests  # Добавляем импорт requests

from src.external_api import convert_transaction_amount  # Импорт тестируемой функции


class TestCurrencyConversion(unittest.TestCase):
    def test_rub_transaction(self):
        """Тест транзакции в RUB (конвертация не требуется)."""
        transaction = {"amount": 1000, "currency": "RUB"}
        result = convert_transaction_amount(transaction)
        self.assertEqual(result, 1000.0)

    @patch("external_api.requests.get")
    def test_usd_conversion(self, mock_get):
        """Тест конвертации USD в RUB."""
        # Мок ответа API
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 90.5}, "success": True}
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_transaction_amount(transaction)
        self.assertEqual(result, 9050.0)  # 100 USD * 90.5

    @patch("external_api.requests.get")
    def test_api_failure(self, mock_get):
        """Тест ошибки API."""
        mock_get.side_effect = requests.RequestException("API error")  # Теперь requests определен
        transaction = {"amount": 100, "currency": "EUR"}
        with self.assertRaises(ValueError):
            convert_transaction_amount(transaction)


if __name__ == "__main__":
    unittest.main()
