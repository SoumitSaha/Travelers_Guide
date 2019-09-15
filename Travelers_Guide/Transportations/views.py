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

from Places.models import Location, Tourist
from Transportations.models import Stand,PublicTransport
from collections import namedtuple


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def user_transportation(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, "transportation.html", {})
    else:
        return redirect('/user/login/')


def transportation_result(request, *args, **kwargs):
    if request.method == 'POST':
        Lat_Src = request.POST.get("lat", "")
        Lon_Src = request.POST.get("lon", "")
        Lat_Dst = request.POST.get("lat_dt", "")
        Lon_Dst = request.POST.get("lon_dt", "")

        lat_src = radians(float(Lat_Src))
        lon_src = radians(float(Lon_Src))
        lat_dst = radians(float(Lat_Dst))
        lon_dst = radians(float(Lon_Dst))

        R = 6373.0
        Data = Location.objects.all()
        has_stand_near_src = 0
        has_stand_near_dst = 0
        for i in Data:
            lat1 = radians(float(i.gps_x))
            lon1 = radians(float(i.gps_y))
            dlon = lon1 - lon_src
            dlat = lat1 - lat_src
            a = sin(dlat / 2) ** 2 + cos(lat_src) * cos(lat1) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if distance <= 1:
                stand_src_obj = Stand.objects.filter(location_id=i.location_id)
                has_stand_near_src = 1
                break

        for i in Data:
            lat2 = radians(float(i.gps_x))
            lon2 = radians(float(i.gps_y))
            dlon = lon2 - lon_dst
            dlat = lat2 - lat_dst
            a = sin(dlat / 2) ** 2 + cos(lat_dst) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if distance <= 1:
                stand_dst_obj = Stand.objects.filter(location_id=i.location_id)
                has_stand_near_dst = 1
                break
        if has_stand_near_dst ==0 or has_stand_near_src == 0:
            message_ = "Sorry no stands near your source or destination."
            k = {
                'msg': message_,
            }
            return render(request, "not_found.html", k)

        else:
             source_stand_name = stand_src_obj[0].stand_name
             dst_stand_name = stand_dst_obj[0].stand_name
             print(source_stand_name)

             source_stand_name_appended = '%' + source_stand_name
             dst_stand_name_appended = '%' + dst_stand_name + '%'

             source_dst_appended = source_stand_name_appended + dst_stand_name_appended
             dst_source_apppended = '%' + dst_stand_name + '%' + source_stand_name + '%'


             cursor = connection.cursor()
             cursor.execute("SELECT * FROM PublicTransports where route like %s or route like %s",[source_dst_appended, dst_source_apppended])
             bus_name = namedtuplefetchall(cursor)
             print(bus_name)

             j = {
                 'bus_number': bus_name,
                 'source_stand': source_stand_name,
                 'dst_stand': dst_stand_name
             }
             print("accha")
             return render(request, "transportation_result.html", j)

    else:
        return redirect('/user/login/')