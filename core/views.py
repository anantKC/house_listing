from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import RedirectView
from django.views.generic.edit import FormView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse

from core.models import HouseListing, WishList, Comment
from core.forms import HouseListingForm, UpdateUser, LoginForm, SignUpForm
from user.models import CustomUser


class ListHouseView(View):
    def get(self, request):
        house_list = HouseListing.objects.all()
        context = {'house_list': house_list}
        return render(request, 'core/home.html', context)


class DetailHouseView(View):
    def get(self, request, id):
        house_list = get_object_or_404(HouseListing, id=id)
        comments = Comment.objects.filter(house_listing=id)
        context = {'house_list': house_list, 'comments': comments}
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
        form = HouseListingForm(
            request.POST, request.FILES, instance=listing, request=request)
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


class SignupView(FormView):
    form_class = SignUpForm
    template_name = 'core/sign_up.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = form.cleaned_data.get('email')
        print("user", user)
        user.save()
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, View):

    def get(self, request):
        form = UpdateUser(instance=request.user)
        context = {'form': form}
        return render(request, 'core/update_profile.html', context)

    def post(self, request):
        form = UpdateUser(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('listhouse')


class UserWishlist(LoginRequiredMixin, View):

    def get(self, request):
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        houses = wishlist.houses.all()
        context = {
            'houses': houses
        }
        return render(request, 'core/wishlist.html', context)


class AddToWishlist(LoginRequiredMixin, View):

    def get(self, request, house_id):
        house = HouseListing.objects.get(id=house_id)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist.houses.add(house)
        return redirect('wishlist')


class RemoveFromWishlist(LoginRequiredMixin, View):

    def get(self, request, house_id):
        house = HouseListing.objects.get(id=house_id)
        wishlist = WishList.objects.get(user=request.user)
        wishlist.houses.remove(house)
        return redirect('wishlist')


class SearchHouseListingView(LoginRequiredMixin, View):

    def get(self, request):
        location = request.GET.get('location')
        listings = HouseListing.search_by_location(location)
        context = {
            'listings': listings
        }
        return render(request, 'core/search_result.html', context)


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('listhouse')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid email or password')
            return self.form_invalid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('listhouse')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    template_name = 'core/create_comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.house_listing = HouseListing.objects.get(
            id=self.kwargs['id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'id': self.kwargs['id']})

# Admin Panel

class UserListView(ListView):
    model = CustomUser
    template_name = 'core/admin/userlist.html'
    context_object_name = 'userlist'

class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'core/admin/deleteuser.html'
    success_url = reverse_lazy('userlist')

class AdminHouseListView(ListView):
    model = HouseListing
    template_name = 'core/admin/houselist.html'
    context_object_name = 'adminhouselist'

class AdminHouseDeleteView(DeleteView):
    model = HouseListing
    template_name = 'core/admin/deletehouselist.html'
    success_url = reverse_lazy('adminhouselist')
