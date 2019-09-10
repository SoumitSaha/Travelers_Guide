from django.contrib import admin
from .models import Location, Place, PlaceReview, Verification, Tourist, Admin, Inbox, PlaceSuggestion

# Register your models here.

admin.site.register(Location)
admin.site.register(Place)
admin.site.register(PlaceReview)
admin.site.register(Verification)
admin.site.register(Tourist)
admin.site.register(Admin)
admin.site.register(PlaceSuggestion)
#admin.site.register(Inbox)
