from django.urls import path
from .views import RandomNumberView

urlpatterns = [
    path('random-number/', RandomNumberView.as_view(), name='random-number'),
]
