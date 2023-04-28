from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import LoginView

from core.models import HouseListing,WishList
from core.forms import HouseListingForm,UpdateUser

# Create your views here.

class ListHouseView(View):
    def get(self, request):
        house_list = HouseListing.objects.all()
        context = {'house_list': house_list}
        return render(request, 'core/home.html', context)

class DetailHouseView(View):
    def get(self, request, id):
        house_list = get_object_or_404(HouseListing, id=id)
        context = {'house_list': house_list}
        return render(request, 'core/detail.html', context)

class CreateListHouseView(View):
    def get(self, request):
        form = HouseListingForm()
        context = {'form': form}
        return render(request, 'core/create_house_list.html', context)

    def post(self, request):
        form = HouseListingForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            return redirect('listhouse')
        else:
            print(form.errors)
        context = {'form': form}
        return render(request, 'core/create_house_list.html', context)

class UpdateListHouseView(View):
    def get(self, request, id):
        listing = get_object_or_404(HouseListing, id=id)
        form = HouseListingForm(instance=listing)
        context = {'form': form, 'listing': listing}
        return render(request, 'core/update_house_list.html', context)

    def post(self, request, id):
        listing = get_object_or_404(HouseListing, id=id)
        form = HouseListingForm(request.POST, request.FILES, instance=listing, request=request)
        if form.is_valid():
            form.save()
            return redirect('listhouse')
        context = {'form': form, 'listing': listing}
        return render(request, 'core/update_house_list.html', context)

class DeleteListHouseView(View):
    def get(self, request, id):
        listing = get_object_or_404(HouseListing, id=id)
        context = {'listing': listing}
        return render(request, 'core/delete.html', context)

    def post(self, request, id):
        listing = get_object_or_404(HouseListing, id=id)
        listing.delete()
        return redirect('listhouse')
    
class SignUpView(View):
    def get(self,request):
        form = UserCreationForm()
        context = {'form':form}
        return render(request,'core/sign_up.html',context)
    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
            context = {'form': form}
            return render(request, 'core/sign_up.html', context)      

class UpdateProfileView(LoginRequiredMixin,View):
    def get(self,request):
        form = UpdateUser(instance = request.user)
        context = {'form': form}
        return render(request,'core/update_profile.html',context)
    def post(self,request):
        form = UpdateUser(request.POST,instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('listhouse')

class UserWishlist(LoginRequiredMixin,View):
    def get(self,request):
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        houses = wishlist.houses.all()
        context = {
            'houses':houses
        }
        return render(request,'core/wishlist.html',context)

class AddToWishlist(LoginRequiredMixin,View):
    def get(self,request,house_id):
        house = HouseListing.objects.get(id=house_id)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist.houses.add(house)
        return redirect('wishlist')

class RemoveFromWishlist(LoginRequiredMixin,View):
    def get(self,request,house_id):
        house = HouseListing.objects.get(id=house_id)
        wishlist = WishList.objects.get(user=request.user)
        wishlist.houses.remove(house)
        return redirect('wishlist')
    
class SearchHouseListingView(LoginRequiredMixin,View):
    def get(self,request):
        location = request.GET.get('location')
        listings = HouseListing.search_by_location(location)
        context = {
            'listings':listings
        }
        return render(request,'core/search_result.html',context)


