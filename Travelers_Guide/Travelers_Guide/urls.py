"""Travelers_Guide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django import urls

from Places.views import admin_login, admin_verification_1, admin_verification_2,  project_home, user_login, user_contact
from Places.views import contact_confirm, admin_inbox, user_home, user_signup, user_add, user_places, place_details, submit_place_review, suggest_place, admin_place_review
from Places.views import place_suggestion_info, admin_place_review_action, user_home_places, user_profile, user_profile_edit_page_show,about
from Places.views import profile_edit_confirm, place_details_without_route

from Restaurants.views import restaurants_details,user_food, user_home_restaurants, restaurants_details_without_route
from Restaurants.views import user_restaurants

from Transportations.views import user_transportation,transportation_result

urlpatterns = [
    path('', project_home, name='projecthome'),
    path('contact/', user_contact, name='contactus'),
    path('contact/confirmed/', contact_confirm , name='contactconfirmed'),
    path('admin/home/default/', admin.site.urls, name='admindefault'),
    path('admin/', admin_login, name='adminlogin'),
    path('admin/home/inbox/', admin_inbox, name='admininbox'),
    path('admin/home/placesuggestion/', admin_place_review, name='adminplacereview'),
    path('admin/home/placesuggestion/action/', admin_place_review_action, name='adminplacereviewaction'),
    path('admin/home/', admin_verification_1, name='adminhome'),
    path('user/login/', user_login, name='userlogin'),
    path('user/home/', user_home, name='userhome'),
    path('user/home/homeplaces/', user_home_places, name='userhomeplaces'),
    path('user/home/homerestaurants/', user_home_restaurants, name='userhomerestaurants'),
    path('user/home/placesuggest/', suggest_place, name='suggestplace'),
    path('user/home/places/', user_places, name='userplaces'),
    path('user/signup/', user_signup, name='usersignup'),
    path('user/signup/done/', user_add, name='useradd'),
    path('user/home/places/details/', place_details, name='placedetails'),
    path('user/home/places/details/wr', place_details_without_route, name='placedetailswithoutroute'),
    path('user/home/restaurants/details/', restaurants_details, name='restaurantsdetails'),
    path('user/home/restaurants/details/wr', restaurants_details_without_route, name='restaurantsdetailswithoutroute'),
    path('user/home/places/details/review/', submit_place_review, name='submitplacereview'),
    path('user/home/placesuggest/validate/', place_suggestion_info, name='placesuggestion'),
    path('user/home/restaurants/', user_restaurants, name='userrestaurants'),
    path('user/home/userfood/', user_food, name='userfood'),
    path('user/home/transportation/', user_transportation, name='usertransportation'),
    path('user/home/transportation/details/', transportation_result, name='transportationresult'),
    path('user/home/profile/', user_profile, name='userprofile'),
    path('user/home/profile/edit', user_profile_edit_page_show, name='userprofileedit'),
    path('user/home/profile/edit/confirm', profile_edit_confirm, name='profileeditconfirm'),
    path('about/', about, name='about'),

]
