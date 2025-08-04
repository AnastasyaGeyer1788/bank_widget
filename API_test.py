import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("EXCHANGE_RATE_API_KEY")
url = "https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols=RUB"
headers = {"apikey": api_key}

response = requests.get(url, headers=headers)
print(response.json())  # возвращает курс USD → RUB
print(os.getenv("EXCHANGE_RATE_API_KEY"))  # выведет мой ключ