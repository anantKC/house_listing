from django.forms import ModelForm
from .models import HouseListing
from django.core.exceptions import PermissionDenied

class HouseListingForm(ModelForm):
    
    class Meta:
        model = HouseListing
        fields = ['image','location','area_in_sqm','price']

    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True, *args, **kwargs):
        # return HouseListing.objects.create(user=self.request.user,**self.cleaned_data)
        instance = super().save(commit=False)
        if not instance.id:
            instance.user = self.request.user
        elif instance.user != self.request.user:
            raise PermissionDenied("You do not have right to update this form")
        if commit:
            instance.save()
        return instance
    
        