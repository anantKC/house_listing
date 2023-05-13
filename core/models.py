from django.db import models
from user.models import CustomUser


class HouseListing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='house_images')
    location = models.CharField(max_length=50)
    area_in_sqm = models.FloatField()
    price = models.IntegerField()

    @staticmethod
    def search_by_location(location):
        return HouseListing.objects.filter(location__contains=location)

    def __str__(self):
        return self.user.email
    

class WishList(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    houses = models.ManyToManyField(HouseListing)

    def __str__(self):
        return self.houses


class Comment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    house_listing = models.ForeignKey(HouseListing,on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField('date_published',auto_now_add=True)
    
    def __str__(self):
        return self.body

    