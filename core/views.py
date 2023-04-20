from django.shortcuts import render, redirect
from .models import HouseListing
from .forms import HouseListingForm,UpdateUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
        form = HouseListingForm(request.POST, request.FILES,instance=listing,request=request)
        if form.is_valid():
            form.save()
            return redirect('listhouse')
            
    context = {'form': form}
    return render(request, 'core/update_house_list.html', context)


def delete_list_house(request, id):
    listing = HouseListing.objects.get(id=id)
    # form = HouseListingForm(instance=listing,request=request)
    # if request.method == 'POST' and 'delete' in request.POST:'
    if request.method == 'POST':
        listing.delete()
        return redirect('listhouse')
    return render(request, 'core/delete.html')

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'core/sign_up.html',context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateUser(request.POST,instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('listhouse')
    else:
        form = UpdateUser(instance = request.user)
    context = {
        'form':form
    }
    return render(request,'core/update_profile.html',context)

