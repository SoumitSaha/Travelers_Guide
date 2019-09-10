from django.db import models
from Places.models import Location


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False)
    gps_x = models.CharField(max_length=250, blank=False)
    gps_y = models.CharField(max_length=250, blank=False)
    opening_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    closing_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True)

    class Meta:
        db_table = "Restaurants"


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    category = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = "Foods"


class FoodAtRestaurants(models.Model):
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)
    sample_pic = models.CharField(max_length=500, blank=False)

    class Meta:
        unique_together = [['food_id', 'restaurant_id']]
        db_table = "Foods_At_Restaurants"
