from django.urls import path
from .views import *
urlpatterns = [
    path('',ListHouseView.as_view(), name='listhouse'),
    path('detail/<str:id>',DetailHouseView.as_view(), name='detail'),
    path('add_house',CreateListHouseView.as_view(), name='createlisthouse'),
    path('update/<str:id>/edit',UpdateListHouseView.as_view(), name='updatelisthouse'),
    path('delete/<str:id>',DeleteListHouseView.as_view(), name='deletelisthouse'),
    path('signup',sign_up,name='signup'),
    path('updateprofile',update_profile,name='updateprofile'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add-to-wishlist/<int:house_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:house_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]