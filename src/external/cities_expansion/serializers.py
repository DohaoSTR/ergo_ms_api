from rest_framework import serializers
from src.external.cities_expansion.models import LocationType, Location, CountryCodeAdjacent

class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = ['location_type_id', 'description']
        read_only_fields = ['location_type_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class LocationSerializer(serializers.ModelSerializer):
    location_type = LocationTypeSerializer(read_only=True)

    class Meta:
        model = Location
        fields = ['location_id', 'name', 'latitude', 'longitude', 'location_type']
        read_only_fields = ['location_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['location_type'] = LocationTypeSerializer(instance.location_type).data
        return representation

class CountryCodeSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CountryCodeAdjacent
        fields = ['location_id', 'country_name', 'a2_code', 'a3_code', 'numeric']
        read_only_fields = ['location_id', 'country_name']
    
    def get_country_name(self, obj):
        return obj.location.name