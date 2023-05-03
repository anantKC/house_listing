from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from user.managers import UserMananger

# Create your models here.

class CustomUser(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=50, default='Anatoly')
    email = models.EmailField(max_length=100,unique=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserMananger()