import requests
from django.utils.timezone import now, make_aware
from external.ETL.analyze.models import BitcoinPrice
import datetime

DEFAULT_DAYS = 10

def fetch_historical_bitcoin_prices(days=None):
    """Функция для получения цен Bitcoin за последние N дней и сохранения в БД."""
    if days is None:
        days = DEFAULT_DAYS

    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}&interval=daily"

    # Полное удаление всех записей перед обновлением
    deleted_count, _ = BitcoinPrice.objects.all().delete()
    print(f"[!] Удалено {deleted_count} старых записей Bitcoin")

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "prices" in data:
            bitcoin_prices = []
            for price_entry in data["prices"]:
                timestamp_ms, price = price_entry
                timestamp = datetime.datetime.utcfromtimestamp(timestamp_ms / 1000)
                timestamp = make_aware(timestamp)
                bitcoin_prices.append(BitcoinPrice(price_usd=price, timestamp=timestamp))

            BitcoinPrice.objects.bulk_create(bitcoin_prices)
            print(f"[+] Добавлено {len(bitcoin_prices)} новых записей Bitcoin")
        else:
            print("[-] Ошибка: отсутствуют данные о ценах")
    else:
        print(f"[-] Ошибка запроса: {response.status_code}")