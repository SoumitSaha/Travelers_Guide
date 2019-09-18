from django.shortcuts import render, redirect
from django.db.models import Q
from math import sin, cos, sqrt, atan2, radians
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, connection
from django.views.decorators.cache import cache_control
from collections import namedtuple

from Restaurants.views import user_restaurants

from .models import Admin, PlaceReview, Tourist, Location, Place, Inbox, PlaceSuggestion

Lat = 0
Lon = 0
User_Id = 0
place_global = 0


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def project_home(request, *args, **kwargs):
    return render(request, "project_home_slide.html", {})


def contact_confirm(request, *args, **kwargs):
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Email = request.POST.get("email", "")
        Message = request.POST.get("message", "")
        i = Inbox(full_name=Name, email=Email, message=Message)
        i.save()
        return render(request, "user_contact_confirm.html", {})

    else:
        return redirect('/user/login/')


def admin_login(request, *args, **kwargs):
    return render(request, "admin_login.html", {})


def admin_verification_2(request, *args, **kwargs):
    if request.method == 'POST':
        Username = request.POST.get("username", "")
        Password = request.POST.get("pass", "")
        user = authenticate(request, username=Username, password=Password)
        if user is not None:
            return redirect('/admin/default')
        else:
            return render(request, "admin_login_again.html", {})


def admin_verification_1(request, *args, **kwargs):
    if request.method == 'GET':
        return redirect('/admin')

    if request.method == 'POST':
        Username = request.POST.get("username", "")
        Password = request.POST.get("pass", "")
        counter = Admin.objects.filter(email=Username, password=Password)

        if counter.count() != 0:
            user = Admin.objects.get(email=Username, password=Password)
            name = user.user_name
            j = {
                'Name': name
            }
            return render(request, "temp.html", j)
        else:
            return render(request, "admin_login_again.html", {})


def admin_inbox(request, *args, **kwargs):
    data = Inbox.objects.all()
    i = {
        'inbox_number': data
    }

    return render(request, "admin_inbox.html", i)


def user_contact(request, *args, **kwargs):
    return render(request, "user_contact.html", {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url='/userlogin')
def user_login(request, *args, **kwargs):
    logout(request)
    request.session.flush()
    return render(request, "user_login.html", {})


def user_signup(request, *args, **kwargs):
    return render(request, "user_signup.html", {})


def user_home_places(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, "user_home_places.html", {})
    else:
        return redirect('/user/login/')


def user_home(request, *args, **kwargs):
    if request.method == 'POST':
        Username = request.POST.get("username", "")
        Password = request.POST.get("pass", "")
        user = authenticate(request, username=Username, password=Password)
        if user is not None:
            login(request, user)

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Places WHERE average_rating>=3.0")
            t_places = namedtuplefetchall(cursor)
            j = {

                'top_places': t_places,
            }
            return render(request, "user_home.html", j)
        else:
            return render(request, "user_login_again.html", {})
    else:
        if request.user.is_authenticated:

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Places WHERE average_rating>=3.0")
            t_places = namedtuplefetchall(cursor)

            j = {

                'top_places': t_places,
            }
            return render(request, "user_home.html", j)
        else:
            return render(request, "user_login_continue.html", {})


def user_places(request, *args, **kwargs):
    if request.method == 'POST':
        option = request.POST.get("option", "")
        if option == "2":
            return user_restaurants(request, *args, **kwargs)
        global Lat
        global Lon
        Lat = request.POST.get("lat", "")
        Lon = request.POST.get("lon", "")
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
                place = Place.objects.filter(location_id=i.location_id)
                has_places = 1
                break
        if has_places == 0:
            message_ = "Sorry , we couldn't find any nearby places."
            k = {
                'msg' : message_,
            }
            return render(request, "not_found.html", k)
        j = {
            'place_number': place,
            'my_loc_gps_x': Lat,
            'my_loc_gps_y': Lon,
        }
        return render(request, "places.html", j)

    else:
        if request.user.is_authenticated:
            return render(request, "places.html", {})
        else:
            return render(request, "user_login_continue.html", {})


def place_details(request, *args, **kwargs):
    if request.method == 'POST':
        global place_global

        Place_Id = request.POST.get("table_data", "")
        place = Place.objects.filter(place_id=Place_Id)
        place_global = Place.objects.get(place_id=Place_Id)
        data = PlaceReview.objects.filter(place_id=place_global)
        rating_sum = 0
        count = 0
        for i in data:
            rating_sum += int(i.rating)
            count += 1

        if count != 0:
            avg_rating = rating_sum / count
        else:
            avg_rating = 0
        global Lat
        global Lon

        j = {
            'avg_rat': avg_rating,
            'place_number': place,
            'my_loc_gps_x': Lat,
            'my_loc_gps_y': Lon,
            'review_number': data
        }
        return render(request, "place_details.html", j)

    else:
        return redirect('/user/login/')


def place_details_without_route(request, *args, **kwargs):
    if request.method == 'POST':
        global place_global

        Place_Id = request.POST.get("table_data", "")
        place = Place.objects.filter(place_id=Place_Id)
        place_global = Place.objects.get(place_id=Place_Id)
        data = PlaceReview.objects.filter(place_id=place_global)
        rating_sum = 0
        count = 0
        for i in data:
            rating_sum += int(i.rating)
            count += 1

        if count != 0:
            avg_rating = rating_sum / count
        else:
            avg_rating = 0

        j = {
            'avg_rat': avg_rating,
            'place_number': place,
            'review_number': data,
            'gps_x' : place_global.gps_x,
            'gps_y' : place_global.gps_y
        }
        return render(request, "place_details_wr.html", j)

    else:
        return redirect('/user/login/')


def user_add(request, *args, **kwargs):
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        User_Name = request.POST.get("username", "")
        Nationality = request.POST.get("nationality", "")
        Passport = request.POST.get("passport", "")
        Email = request.POST.get("email", "")
        Gender = request.POST.get("gender", "")
        Password = request.POST.get("pass", "")
        RePassword = request.POST.get("repass", "")
        found = Tourist.objects.filter(Q(email=Email) | Q(passport_no=Passport))
        found1 = User.objects.filter(Q(username=User_Name))
        if Password != RePassword:
            return render(request, "user_add_password_mismatch.html", {})

        if found.count() == 0 & found1.count() == 0:
            try:
                user = User.objects.create_user(User_Name, Email, Password)
                i = Tourist(name=Name, user_name=User_Name, nationality=Nationality, passport_no=Passport, email=Email,
                            gender=Gender, )
                i.save()
                user.save()
                return render(request, "user_add_confirm.html", {})

            except IntegrityError as e:
                return render(request, "user_add_email_used.html", {})



        else:
            return render(request, "user_add_email_used.html", {})

    else:
        return redirect('/user/login/')


def submit_place_review(request, *args, **kwargs):
    if request.method == 'POST':
        Rating = request.POST.get("rating", "")
        Comment = request.POST.get("comment", "")
        global place_global

        Name = Tourist.objects.get(user_name=request.user)
        found = PlaceReview.objects.filter(Q(tourist_id=Name), Q(place_id=place_global))
        if found.count() == 0:
            i = PlaceReview(place_id=place_global, tourist_id=Name, tourist_name=Name.name, rating=Rating,
                            comment=Comment)
            i.save()

            rating_sum = 0
            count = 0
            data = PlaceReview.objects.filter(place_id=place_global)
            for i in data:
                rating_sum += int(i.rating)
                count += 1

            if count != 0:
                avg_rating = rating_sum / count
            else:
                avg_rating = 0

            obj = Place.objects.get(place_id=place_global.place_id)
            obj.average_rating = avg_rating
            obj.save()


            j = {
                'msg': "Thank you for your review"
            }
            return render(request, "review_confirm.html", j)
        else:
            i = PlaceReview.objects.get(tourist_id=Name, place_id=place_global)
            i.rating = Rating
            i.comment = Comment
            i.save()

            rating_sum = 0
            count = 0
            data = PlaceReview.objects.filter(place_id=place_global)
            for i in data:
                rating_sum += int(i.rating)
                count += 1

            if count != 0:
                avg_rating = rating_sum / count
            else:
                avg_rating = 0

            obj = Place.objects.get(place_id=place_global.place_id)
            obj.average_rating = avg_rating
            obj.save()
            j = {
                'msg': "Your review has been updated"
            }
            return render(request, "review_confirm.html", j)

    else:
        return redirect('/user/login/')


def suggest_place(request, *args, **kwargs):
    if request.user.is_authenticated:
        return render(request, "suggest_place.html", {})
    else:
        return redirect('/user/login/')



def place_suggestion_info(request, *args, **kwargs):
    if request.method == 'POST':
        GPS_X = request.POST.get("gps_x", "")
        GPS_Y = request.POST.get("gps_y", "")
        Name = request.POST.get("name", "")
        Category = request.POST.get("category", "")
        Opening_Time = request.POST.get("opening_time", "")
        Closing_Time = request.POST.get("closing_time", "")
        OffDay = request.POST.get("offday", "")
        Sample_Pic = request.POST.get("sample_pic", "")

        lat1 = radians(float(GPS_X))
        lon1 = radians(float(GPS_Y))
        R = 6373.0
        Data = Location.objects.all()
        has_location = 0
        loc_id = 0
        for i in Data:
            lat2 = radians(float(i.gps_x))
            lon2 = radians(float(i.gps_y))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c

            if distance <= 1:
                location = Location.objects.get(location_id=i.location_id)
                loc_id = int(location.location_id)
                has_location = 1
                break
        if has_location == 0:
            j = {
                'msg': "Your suggested place is not in our service area"
            }
            return render(request, "review_confirm.html", j)
        else:
            already_in_place = 0
            if loc_id != 0:
                places = Place.objects.filter(location_id=loc_id)

                for k in places:
                    lat2 = radians(float(k.gps_x))
                    lon2 = radians(float(k.gps_y))
                    dlon = lon2 - lon1
                    dlat = lat2 - lat1
                    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))

                    distance = R * c

                    if distance < 0.2:
                        already_in_place = 1

            if already_in_place != 0:
                j = {
                    'msg': "Place already registered"
                }
            else:
                i = PlaceSuggestion(suggested_location_id=int(location.location_id), name=Name, category=Category,
                                    gps_x=GPS_X, gps_y=GPS_Y, opening_time=Opening_Time, closing_time=Closing_Time,
                                    offday=OffDay, sample_pic=Sample_Pic)
                i.save()

                j = {
                    'msg': "Your suggestion has been received. Thank You"
                }
            return render(request, "review_confirm.html", j)

    else:
        return redirect('/user/login/')





def admin_place_review(request, *args, **kwargs):
    data = PlaceSuggestion.objects.all()
    i = {
        'suggestion_number': data
    }
    return render(request, "admin_place_suggestion.html", i)


def admin_place_review_action(request, *args, **kwargs):
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Category = request.POST.get("category", "")
        Loc_id = request.POST.get("location_id", "")
        Loc = Location.objects.get(location_id=Loc_id)
        X = request.POST.get("gps_x", "")
        Y = request.POST.get("gps_y", "")
        Open = request.POST.get("opening_time", "")
        Close = request.POST.get("closing_time", "")
        Offday = request.POST.get("offday", "")
        Pic_url = request.POST.get("sample_pic", "")
        Op_val = request.POST.get("operation", "")
        save = 0
        if Op_val == 'add':
            if Open != '0':
                if Offday != '0':
                    i = Place(location_id=Loc, name=Name, category=Category, gps_x=X, gps_y=Y,
                              opening_time=Open, closing_time=Close, offday=Offday, sample_pic=Pic_url)
                else:
                    i = Place(location_id=Loc, name=Name, category=Category, gps_x=X, gps_y=Y,
                              opening_time=Open, closing_time=Close, sample_pic=Pic_url)
            else:
                if Offday != '0':
                    i = Place(location_id=Loc, name=Name, category=Category, gps_x=X, gps_y=Y,
                              offday=Offday, sample_pic=Pic_url)
                else:
                    i = Place(location_id=Loc, name=Name, category=Category, gps_x=X, gps_y=Y,
                              sample_pic=Pic_url)
            i.save()
            save = 1

        data = PlaceSuggestion.objects.get(Q(gps_x=X), Q(gps_y=Y))
        data.delete()

        if save == 1:
            j = {
                'msg': "Place added to Database."
            }
        else:
            j = {
                'msg': "Place Discarded."
            }
        return render(request, "admin_action_confirm.html", j)



def user_profile(request, *args, **kwargs):
    if request.user.is_authenticated:
        user_ = Tourist.objects.get(user_name=request.user.username)
        i ={
            'tourist': user_,
        }
        return render(request, "profile.html", i)

    else :
        return render(request, "user_login_continue.html", {})


def user_profile_edit_page_show(request, *args, **kwargs):
    if request.user.is_authenticated:
        user_ = Tourist.objects.get(user_name=request.user)
        i = {
            'tourist': user_,
        }
        return render(request, "profile_edit.html", i)

    else :
        return render(request, "user_login_continue.html", {})


def about(request, *args, **kwargs):
    return render(request, "about.html", {})


def profile_edit_confirm(request, *args, **kwargs):
    if request.method == 'POST':
        Name = request.POST.get("new_name", "")
        Email = request.POST.get("new_email", "")
        Passport = request.POST.get("new_passport", "")
        Password = request.POST.get("new_password", "")
        Conf_Password = request.POST.get("new_conf_password", "")

        if Password != Conf_Password:
            user_ = Tourist.objects.get(user_name=request.user)
            j = {
                'tourist': user_,
                'msg': "Passwords didnot match"
            }
            return render(request, "profile_edit.html", j)

        else:
            tourist = Tourist.objects.get(user_name=request.user)
            user = User.objects.get(username=request.user)

            tourist.name = Name
            tourist.email =Email
            tourist.passport_no = Passport
            user.set_password(Password)

            tourist.save()
            user.save()

            return render(request, "profile_edit_confirm.html", {})

    else:
        return redirect('/user/home/profile/')


