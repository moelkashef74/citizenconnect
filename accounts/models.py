from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator



class User(AbstractBaseUser, PermissionsMixin):
    first_name= models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name= models.CharField(max_length=100, verbose_name=_("Last Name"))
    email_or_phone = models.CharField(max_length=255, unique=True, verbose_name=_("Email Address or Phone Number"),
                                      validators=[RegexValidator(
                                          regex=r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$|^[\d\-\+\(\) ]+$',
                                          message=_('Enter a valid email address or phone number.'),
                                      )])
    id= models.CharField(max_length=14, unique=True, primary_key=True, verbose_name=_('Id'))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email_or_phone'

    REQUIRED_FIELDS = ["first_name", "last_name", "id"]

    objects= UserManager()

    
    def __str__(self):
        return self.email_or_phone
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def tokens(self):
         refresh = RefreshToken.for_user(self)
         return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

