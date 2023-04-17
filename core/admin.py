from django.contrib import admin
from .models import HouseListing
# Register your models here.

class HouseListingAdmin(admin.ModelAdmin):
    list_display = ('area_in_sqm','price')

admin.site.register(HouseListing,HouseListingAdmin)
