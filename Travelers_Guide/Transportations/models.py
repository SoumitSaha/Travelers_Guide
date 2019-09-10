from django.db import models
from Places.models import Location


class Stand(models.Model):
    stand_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, blank=False)
    gps_x = models.CharField(max_length=250, blank=False)
    gps_y = models.CharField(max_length=250, blank=False)

    class Meta:
        db_table = "Stands"


class StandToStandCommunication(models.Model):
    stand1_id = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    stand2_id = models.ForeignKey(Stand, on_delete=models.CASCADE)
    vehicle_description = models.CharField(max_length=800, blank=False)

    class Meta:
        unique_together = [['stand1_id', 'stand2_id']]
        db_table = "Stand_To_Stand"
