from django.core.management.base import BaseCommand
from external.ETL.analyze.scripts import fetch_historical_bitcoin_prices, DEFAULT_DAYS

class Command(BaseCommand):
    help = f"Получает цену биткоина за последние {DEFAULT_DAYS} дней и сохраняет в БД"

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=DEFAULT_DAYS, help="Количество дней для загрузки")

    def handle(self, *args, **options):
        days = options['days']  # Получаем значение из аргумента
        fetch_historical_bitcoin_prices(days=days)  # Передаём `days` в функцию
        self.stdout.write(self.style.SUCCESS(f"Цены биткоина за последние {days} дней успешно обновлены"))
