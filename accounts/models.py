from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken



class User(AbstractBaseUser, PermissionsMixin):
    first_name= models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name= models.CharField(max_length=100, verbose_name=_("Last Name"))
    email= models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    id= models.CharField(max_length=14, unique=True, primary_key=True, verbose_name=_('Id'))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["first_name", "last_name", "id"]

    objects= UserManager()

    
    def __str__(self):
        return self.email or 'Unknown User'
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def tokens(self):
         refresh = RefreshToken.for_user(self)
         return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

