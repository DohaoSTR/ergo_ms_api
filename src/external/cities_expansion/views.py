from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.external.cities_expansion.models import Location, LocationType, CountryCodeAdjacent
from src.external.cities_expansion.serializers import LocationSerializer, CountryCodeSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Schema, Items, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg import openapi

class CitiesView(APIView):
    @swagger_auto_schema(
        operation_description="Получение информации о доступных городах",
        responses={
            200: openapi.Response(
                description="Список городов",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'cities': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'location_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'longitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'location_type': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'location_type_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                                        }
                                    )
                                }
                            )
                        )
                    }
                )
            )
        }
    )

    def get(self, request, *args, **kwargs):
        cities = Location.objects.filter(location_type__name=LocationType.LocationTypeChoices.CITY.value)
        serializer = LocationSerializer(cities, many=True)
        data = {"cities": serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    
class CountriesView(APIView):
    @swagger_auto_schema(
        operation_description="Получение информации о доступных странах",
        responses={
            200: openapi.Response(
                description="Список стран",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'countries': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'location_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'longitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'location_type': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'location_type_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                                        }
                                    )
                                }
                            )
                        )
                    }
                )
            )
        }
    )

    def get(self, request, *args, **kwargs):
        countries = Location.objects.filter(location_type__name=LocationType.LocationTypeChoices.COUNTRY.value)
        serializer = LocationSerializer(countries, many=True)
        data = {"countries": serializer.data}
        return Response(data, status=status.HTTP_200_OK)

class CountryCodesView(APIView):
    @swagger_auto_schema(
        operation_description="Получение информации о доступных кодах стран",
        responses={
            200: openapi.Response(
                description="Список кодов стран",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'country_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'location_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'country_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'a2_code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'a3_code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'numeric': openapi.Schema(type=openapi.TYPE_INTEGER)
                                }
                            )
                        )
                    }
                )
            )
        }
    )

    def get(self, request, *args, **kwargs):
        country_codes = CountryCodeAdjacent.objects.all()
        serializer = CountryCodeSerializer(country_codes, many=True)
        data = {"country_codes": serializer.data}
        return Response(data, status=status.HTTP_200_OK)