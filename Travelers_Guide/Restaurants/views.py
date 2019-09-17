from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db.models import Q
from math import sin, cos, sqrt, atan2, radians
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, connection
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

from Restaurants.models import Restaurant, FoodAtRestaurants, Food
from Places.models import Location, Tourist
from collections import namedtuple


def wraper(request, *args, **kwargs):
    return redirect(request, '/user/home/restaurants')

def wraper2(request, *args, **kwargs):
    return redirect(request, '/user/home/userfood')

def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def user_home_restaurants(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, "user_home_restaurants.html", {})
    else:
        return redirect('/user/login/')


def user_restaurants(request, *args, **kwargs):
    print(request.method)
    if request.method == 'POST':
        global Lat
        global Lon
        Lat = request.POST.get("lat2", "")
        Lon = request.POST.get("lon2", "")
        lat1 = radians(float(Lat))
        lon1 = radians(float(Lon))
        R = 6373.0
        Data = Location.objects.all()
        has_places = 0
        for i in Data:
            lat2 = radians(float(i.gps_x))
            lon2 = radians(float(i.gps_y))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if distance <= 1:
                restaurant = Restaurant.objects.filter(location_id=i.location_id)
                has_places = 1
                break
        if has_places == 0:
            message_ = "Sorry , we couldn't find any nearby restaurants."
            k = {
                'msg': message_,
            }
            return render(request, "not_found.html", k)
        j = {
            'place_number': restaurant,
            'my_loc_gps_x': Lat,
            'my_loc_gps_y': Lon,
        }
        print(j)
        return render(request, "restaurants.html", j)

    else:
        if request.user.is_authenticated:
            return render(request, "restaurant.html", {})
        else:
            return render(request, "user_login_continue.html", {})


def restaurants_details(request, *args, **kwargs):
    if request.method == 'POST':

        print(request.POST.get("table_data", ""))
        global restaurant_global
        global User_Id
        Restaurant_Id = request.POST.get("table_data", "")
        restaurant = Restaurant.objects.filter(restaurant_id=Restaurant_Id)
        restaurant_global = Restaurant.objects.get(restaurant_id=Restaurant_Id)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Foods JOIN (SELECT FR.food_id_id AS 'foodid', FR.price as 'price', "
                       "FR.sample_pic as 'pic' FROM Foods_At_Restaurants FR JOIN Restaurants R ON "
                       "(R.restaurant_id = FR.restaurant_id_id) "
                       "WHERE restaurant_id =%s) T ON (T.foodid = Foods.food_id)", [int(Restaurant_Id)])
        foods_ = namedtuplefetchall(cursor)

        global Lat
        global Lon

        j = {
            'food_number': foods_,
            'place_number': restaurant,
            'my_loc_gps_x': Lat,
            'my_loc_gps_y': Lon,
        }
        return render(request, "restaurants_details.html", j)

    else:
        return redirect('/user/login/')




def restaurants_details_without_route(request, *args, **kwargs):
    if request.method == 'POST':

        print(request.POST.get("table_data", ""))
        global restaurant_global
        global User_Id
        Restaurant_Id = request.POST.get("table_data", "")
        restaurant = Restaurant.objects.filter(restaurant_id=Restaurant_Id)
        restaurant_global = Restaurant.objects.get(restaurant_id=Restaurant_Id)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Foods JOIN (SELECT FR.food_id_id AS 'foodid', FR.price as 'price', "
                       "FR.sample_pic as 'pic' FROM Foods_At_Restaurants FR JOIN Restaurants R ON "
                       "(R.restaurant_id = FR.restaurant_id_id) "
                       "WHERE restaurant_id =%s) T ON (T.foodid = Foods.food_id)", [int(Restaurant_Id)])
        foods_ = namedtuplefetchall(cursor)

        global Lat
        global Lon

        j = {
            'food_number': foods_,
            'place_number': restaurant,
            'my_loc_gps_x': restaurant_global.gps_x,
            'my_loc_gps_y': restaurant_global.gps_y
        }
        return render(request, "restaurants_details_wr.html", j)

    else:
        return redirect('/user/login/')



def user_food(request, *args, **kwargs):
    if request.method == 'POST':
        food_name = request.POST.get("food", "")
        global Lat
        global Lon
        Lat = request.POST.get("lat3", "")
        Lon = request.POST.get("lon3", "")
        print(Lat)
        lat1 = radians(float(Lat))
        lon1 = radians(float(Lon))
        R = 6373.0
        Data = Location.objects.all()
        has_places = 0
        for i in Data:
            lat2 = radians(float(i.gps_x))
            lon2 = radians(float(i.gps_y))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if distance <= 1:
                restaurant = Restaurant.objects.filter(location_id=i.location_id)
                has_places = 1
                break
        if has_places == 0:
            message_ = "Sorry , we couldn't find any nearby restaurants with your searched food."
            k = {
                'msg': message_,
            }
            return render(request, "not_found.html", k)

        Food_Id = Food.objects.filter(name=food_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Restaurants JOIN (SELECT * FROM Foods_At_Restaurants JOIN "
                       "(SELECT food_id, category, description FROM Foods WHERE name = %s) T ON "
                       "(T.food_id = Foods_At_Restaurants.food_id_id))"
                       " Q On (Q.restaurant_id_id = Restaurants.restaurant_id)", [food_name])
        foods_ = namedtuplefetchall(cursor)

        j = {
            'food_number': foods_,
            'my_loc_gps_x': Lat,
            'my_loc_gps_y': Lon,
            'food_name' : food_name,
        }
        return render(request, "food_search.html", j)

    else:
        return redirect('/user/login/')








