from django.db import models

class BitcoinPrice(models.Model):
    timestamp = models.DateTimeField()
    price_usd = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.timestamp}: ${self.price_usd}"
