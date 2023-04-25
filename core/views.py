from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from core.models import HouseListing,WishList
from core.forms import HouseListingForm,UpdateUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import View
# Create your views here.

# def list_house(request):
#     house_list = HouseListing.objects.all()
#     context = {'house_list': house_list}
#     return render(request, 'core/home.html', context)


# def detail_house(request, id):
#     house_list = HouseListing.objects.get(id=id)
#     context = {'house_list': house_list}
#     return render(request, 'core/detail.html', context)


# def create_list_house(request):
#     form = HouseListingForm()
#     if request.method == 'POST':
#         form = HouseListingForm(request.POST, request.FILES,request=request)
#         if form.is_valid():
#             form.save()
#             return redirect('listhouse')
#         print(form.errors)
#     context = {'form': form}
#     return render(request, 'core/create_house_list.html', context)


# def update_list_house(request, id):
#     listing = HouseListing.objects.get(id=id)
#     form = HouseListingForm(instance=listing)
#     if request.method == 'POST':
#         form = HouseListingForm(request.POST, request.FILES,instance=listing,request=request)
#         if form.is_valid():
#             form.save()
#             return redirect('listhouse')
            
#     context = {'form': form,
#                'listing':listing}
#     return render(request, 'core/update_house_list.html', context)


# def delete_list_house(request, id):
#     listing = HouseListing.objects.get(id=id)
#     # form = HouseListingForm(instance=listing,request=request)
#     # if request.method == 'POST' and 'delete' in request.POST:'
#     if request.method == 'POST':
#         listing.delete()
#         return redirect('listhouse')
#     context = {
#         'listing':listing
#     }
#     return render(request, 'core/delete.html',context)





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

@login_required
def wishlist(request):
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    houses = wishlist.houses.all()
    context = {'houses': houses}
    return render(request, 'core/wishlist.html', context)

@login_required
def add_to_wishlist(request, house_id):
    house = HouseListing.objects.get(id=house_id)
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    wishlist.houses.add(house)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request,house_id):
    house = HouseListing.objects.get(id=house_id)
    wishlist = WishList.objects.get(user=request.user)
    wishlist.houses.remove(house)
    return redirect('wishlist')



