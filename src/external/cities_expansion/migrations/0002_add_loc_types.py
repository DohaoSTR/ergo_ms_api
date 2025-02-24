from django.db import migrations

def add_location_types(apps, schema_editor):
    LocationType = apps.get_model('cities_expansion', 'LocationType')
    LocationType.objects.bulk_create([
        LocationType(name='City', description='Местность является городом'),
        LocationType(name='Region', description='Местность является регионом страны'),
        LocationType(name='Country', description='Местность является страной'),
        LocationType(name='City Region', description='Местность является районом города'),
        LocationType(name='Point', description='Местность представлена координатами'),
        LocationType(name='Continent', description='Местность представлена континентом'),
    ])

class Migration(migrations.Migration):
    dependencies = [
        ('cities_expansion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_location_types),
    ]