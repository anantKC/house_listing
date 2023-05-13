from django.contrib import admin
from .models import HouseListing,WishList,Comment
# Register your models here.

# class HouseListingAdmin(admin.ModelAdmin):
#     list_display = ('area_in_sqm','price')

admin.site.register(HouseListing)
admin.site.register(WishList)
admin.site.register(Comment)
