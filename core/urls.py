from django.urls import path
from .views import *


urlpatterns = [
    path('',ListHouseView.as_view(), name='listhouse'),
    path('detail/<str:id>',DetailHouseView.as_view(), name='detail'),
    path('add_house',CreateListHouseView.as_view(), name='createlisthouse'),
    path('update/<str:id>/edit',UpdateListHouseView.as_view(), name='updatelisthouse'),
    path('delete/<str:id>',DeleteListHouseView.as_view(), name='deletelisthouse'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/',SignupView.as_view(),name='signup'),
    path('updateprofile/',UpdateProfileView.as_view(),name='updateprofile'),
    path('wishlist/', UserWishlist.as_view(), name='wishlist'),
    path('add-to-wishlist/<int:house_id>/', AddToWishlist.as_view(), name='add_to_wishlist'),
    path('remove-from-wishlist/<int:house_id>/', RemoveFromWishlist.as_view(), name='remove_from_wishlist'),
    path('search/',SearchHouseListingView.as_view(),name="search"),
]