from django.urls import path
from .views import BitcoinPriceListAPIView, ExecuteCommandAPIView

urlpatterns = [
    path('bitcoin-price/', BitcoinPriceListAPIView.as_view(), name='bitcoin-price-list'),
    path('execute-command/', ExecuteCommandAPIView.as_view(), name='execute-command'),
]
