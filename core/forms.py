from django.forms import ModelForm
from django import forms
from .models import HouseListing
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

from user.models import CustomUser

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


class UpdateUser(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email','password',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('name','email', 'password1','password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email address already exists.')
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
        