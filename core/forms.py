from django.forms import ModelForm
from django import forms
from .models import HouseListing
from django.core.exceptions import PermissionDenied

class HouseListingForm(ModelForm):
    
    class Meta:
        model = HouseListing
        fields = ['image','location','area_in_sqm','price']

    def clean(self):
        cleaned_data = super().clean()
        area_in_sqm = cleaned_data.get('area_in_sqm')
        price = cleaned_data.get('price')

        if area_in_sqm > 1000:
            raise forms.ValidationError('Area cant be 1000 or above')
        if price < 1000 or price > 10000:
            raise forms.ValidationError("Price should be between 1000 and 10000")

    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        # return HouseListing.objects.create(user=self.request.user,**self.cleaned_data)
        instance = super().save(commit=False)
        instance.user = self.request.user
        if commit:
            instance.save()
        return instance
    
    # def delete(self):
    #     instance = self.instance
    #     if instance.user != self.request.user:
    #         raise PermissionDenied("You do not have right to delete this form")
    #     instance.delete()

    
    
        