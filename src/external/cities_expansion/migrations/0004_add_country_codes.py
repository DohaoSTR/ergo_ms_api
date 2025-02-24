import csv
import os
from django.db import migrations

from src.external.cities_expansion.models import CountryCodeAdjacent

def import_csv(apps, schema_editor):
    CountryCodeAdjacent = apps.get_model('cities_expansion', 'CountryCodeAdjacent')
    csv_file = 'src/external/cities_expansion/migrations/csv/country_codes.csv'

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            CountryCodeAdjacent.objects.create(
                location_id=row['location_id'],
                a2_code=row['a2_code'],
                a3_code=row['a3_code'],
                numeric=row['numeric'],
            )

def reverse_import(apps, schema_editor):
    Location = apps.get_model('cities_expansion', 'CountryCodeAdjacent')
    Location.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('cities_expansion', '0003_add_locations'),
    ]

    operations = [
        migrations.RunPython(import_csv, reverse_import),
    ]