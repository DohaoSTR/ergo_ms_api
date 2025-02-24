from django.urls import path

from src.external.cities_expansion.views import CitiesView , CountriesView

urlpatterns = [
    path('cities/', CitiesView.as_view(), name='cities'),
    path('countries/', CountriesView.as_view(), name='countries')
]