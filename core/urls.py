from django.urls import path
from .views import *
urlpatterns = [
    path('',list_house, name='listhouse'),
    path('detail/<str:id>',detail_house, name='detail'),
    path('add_house',create_list_house, name='createlisthouse'),
    path('update/<str:id>/edit',update_list_house, name='updatelisthouse'),
    path('delete/<str:id>',delete_list_house, name='deletelisthouse'),
    path('signup',sign_up,name='signup')
]