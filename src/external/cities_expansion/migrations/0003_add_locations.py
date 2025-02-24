import csv
import os
from django.db import migrations

from src.external.cities_expansion.models import Location, LocationType

def import_csv(apps, schema_editor):
    Location = apps.get_model('cities_expansion', 'Location')
    csv_file = 'src/external/cities_expansion/migrations/csv/locations.csv'

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Location.objects.create(
                location_id=row['location_id'],
                name=row['name'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                location_type_id=row['location_type_id']
            )

def reverse_import(apps, schema_editor):
    Location = apps.get_model('cities_expansion', 'Location')
    Location.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('cities_expansion', '0002_add_loc_types'),
    ]

    operations = [
        migrations.RunPython(import_csv, reverse_import),
    ]