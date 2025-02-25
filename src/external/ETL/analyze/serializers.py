from rest_framework import serializers
from .models import BitcoinPrice

class BitcoinPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitcoinPrice
        fields = ['timestamp', 'price_usd']
        ref_name = 'BitcoinPriceSerializer_External'  # Уникальное имя
