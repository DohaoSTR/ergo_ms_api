from django.db import models

class LocationType(models.Model):
    class LocationTypeChoices(models.TextChoices):
        CITY = 'City', 'Местность является городом'
        REGION = 'Region', 'Местность является регионом страны'
        COUNTRY = 'Country', 'Местность является страной'
        CITY_REGION = 'City Region', 'Местность является районом города'
        POINT = 'Point', 'Местность представлена координатами'
        CONTINENT = 'Continent', 'Местность представлена континентом'

    location_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, choices=LocationTypeChoices.choices, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_type = models.ForeignKey(LocationType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CountryCodeAdjacent(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    a2_code = models.CharField(max_length=5)
    a3_code = models.CharField(max_length=5)
    numeric = models.IntegerField()

    def __str__(self):
        return f"{self.location.name} ({self.a3_code})"

class BoundingBox(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    bottom_left_latitude = models.FloatField()
    bottom_left_longitude = models.FloatField()
    upper_right_latitude = models.FloatField()
    upper_right_longitude = models.FloatField()

    def __str__(self):
        return f"Bounding Box for {self.location.name}"