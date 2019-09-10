from django.db import models
from Places.models import Location


class Stand(models.Model):
    stand_id = models.AutoField(primary_key=True)
    stand_name = models.CharField(max_length=30, blank=False, default="")
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, blank=False)
    gps_x = models.CharField(max_length=250, blank=False)
    gps_y = models.CharField(max_length=250, blank=False)

    class Meta:
        db_table = "Stands"


class PublicTransport(models.Model):
    transport_id = models.AutoField(primary_key=True)
    transport_name = models.CharField(max_length=30, blank=False)
    category = models.CharField(max_length=30, blank=False)
    route = models.CharField(max_length=1000, blank=False)

    class Meta:
        db_table = "PublicTransports"