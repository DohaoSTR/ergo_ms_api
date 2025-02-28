import csv
import os
from django.db import migrations

from src.external.cities_expansion.models import BoundingBox

def import_csv(apps, schema_editor):
    BoundingBox = apps.get_model('cities_expansion', 'BoundingBox')
    csv_file = 'src/external/cities_expansion/migrations/csv/bounding_boxes.csv'

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            BoundingBox.objects.create(
                location_id=row['location_id'],
                bottom_left_latitude=row['bottom_left_latitude'],
                bottom_left_longitude=row['bottom_left_longitude'],
                upper_right_latitude=row['upper_right_latitude'],
                upper_right_longitude=row['upper_right_longitude']
            )

def reverse_import(apps, schema_editor):
    BoundingBox = apps.get_model('cities_expansion', 'BoundingBox')
    BoundingBox.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('cities_expansion', '0004_add_country_codes'),
    ]

    operations = [
        migrations.RunPython(import_csv, reverse_import),
    ]