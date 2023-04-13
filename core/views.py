from django.shortcuts import render, redirect
from .models import HouseListing
from .forms import HouseListingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
# Create your views here.


def list_house(request):
    house_list = HouseListing.objects.all()
    context = {'house_list': house_list}
    return render(request, 'core/home.html', context)


def detail_house(request, id):
    house_list = HouseListing.objects.get(id=id)
    context = {'house_list': house_list}
    return render(request, 'core/detail.html', context)


def create_list_house(request):
    form = HouseListingForm()
    if request.method == 'POST':
        form = HouseListingForm(request.POST, request.FILES,request=request)
        if form.is_valid():
            form.save()
            
            return redirect('listhouse')
        print(form.errors)
    context = {'form': form}
    return render(request, 'core/create_house_list.html', context)


def update_list_house(request, id):
    listing = HouseListing.objects.get(id=id)
    form = HouseListingForm(instance=listing)
    if request.method == 'POST':
        form = HouseListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listhouse')
    context = {'form': form}
    return render(request, 'core/update_house_list.html', context)


def delete_list_house(request, id):
    listing = HouseListing.objects.get(id=id)
    if request.method == 'POST':
        listing.delete()
        return redirect('listhouse')
    context = {'listing': listing}

    return render(request, 'core/delete.html', context,)

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'core/sign_up.html',context)
