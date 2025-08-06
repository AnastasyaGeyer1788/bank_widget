import pytest
import pandas as pd


@pytest.fixture
def mock_csv_data():
    """Фикстура с тестовыми данными для CSV."""
    return "date,amount,description\n2023-01-01,100,Payment"


@pytest.fixture
def mock_excel_data():
    """Фикстура с тестовыми данными для Excel."""
    return pd.DataFrame({
        'date': ['2023-01-02'],
        'amount': [200],
        'description': ['Deposit']
    })
