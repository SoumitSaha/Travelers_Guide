from django.db import models


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    gps_x = models.CharField(max_length=250, blank=False)
    gps_y = models.CharField(max_length=250, blank=False)

    class Meta:
        db_table = "Locations"


class Tourist(models.Model):
    tourist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    user_name = models.CharField(max_length=250, blank=False)
    nationality = models.CharField(max_length=50, blank=False)
    passport_no = models.CharField(max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=False)
    email = models.EmailField(max_length=254, blank=False)

    class Meta:
        db_table = "Tourists"


class Verification(models.Model):
    temp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    nationality = models.CharField(max_length=50, blank=False)
    passport_no = models.CharField(max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    password = models.CharField(max_length=20, blank=False)
    otp = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        db_table = "Verifications"


class Place(models.Model):
    place_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False)
    category = models.CharField(max_length=50, blank=False)
    average_rating = models.CharField(max_length=1, blank=False, default=0)
    gps_x = models.CharField(max_length=250, blank=False)
    gps_y = models.CharField(max_length=250, blank=False)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    offday = models.CharField(max_length=10, blank=True, null=True)
    sample_pic = models.CharField(max_length=500, blank=False)

    class Meta:
        db_table = "Places"


class PlaceSuggestion(models.Model):
    suggestion_id = models.AutoField(primary_key=True)
    suggested_location_id = models.CharField(max_length=6, blank=False)
    name = models.CharField(max_length=250, blank=False)
    category = models.CharField(max_length=50, blank=False)
    gps_x = models.CharField(max_length=250, blank=False)
    gps_y = models.CharField(max_length=250, blank=False)
    opening_time = models.CharField(max_length=8, blank=True, null=True)
    closing_time = models.CharField(max_length=8, blank=True, null=True)
    offday = models.CharField(max_length=10, blank=True, null=True)
    sample_pic = models.CharField(max_length=500, blank=False)

    class Meta:
        db_table = "PlaceSuggestions"


class PlaceReview(models.Model):
    place_review_id = models.AutoField(primary_key=True)
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    tourist_id = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    tourist_name = models.CharField(max_length=250, blank=False)
    rating = models.CharField(max_length=1, blank=False)
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = "Place_Reviews"


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=25, blank=False)
    email = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "Admins"


class Inbox(models.Model):
    msg_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=75, blank=False)
    email = models.CharField(max_length=100, blank=False)
    message = models.CharField(max_length=1000, blank=False)

    class Meta:
        db_table = "Inboxes"
