from django.contrib import admin
from.models import Restaurant,Food,FoodAtRestaurants

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(FoodAtRestaurants)
