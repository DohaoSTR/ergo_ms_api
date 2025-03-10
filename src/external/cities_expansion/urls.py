from django.urls import path

from src.external.cities_expansion.views import CitiesView , CountriesView, CountryCodesView, BoundingBoxesView

urlpatterns = [
    path('cities/', CitiesView.as_view(), name='cities'),
    path('countries/', CountriesView.as_view(), name='countries'),
    path('country-codes/', CountryCodesView.as_view(), name='country-codes'),
    path('bounding-boxes/', BoundingBoxesView.as_view(), name='bounding-boxes'),
]