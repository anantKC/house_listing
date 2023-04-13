from django.forms import ModelForm
from .models import HouseListing

class HouseListingForm(ModelForm):
    
    class Meta:
        model = HouseListing
        fields = ['image','location','area_in_sqm','price']

    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        return HouseListing.objects.create(user= self.request.user,**self.cleaned_data)



