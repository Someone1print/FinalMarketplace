from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField('email addres', unique=True )
    password = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_Vendor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


class Vendor(MyUser):
    name = models.CharField(max_length=255, null=False, blank=False)
    second_name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.second_name}'


class Customer(MyUser):
    name = models.CharField(max_length=255, null=False, blank=False)
    second_name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    cart_number = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    post_code = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.name}, {self.second_name}'

