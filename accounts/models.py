from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files.storage import default_storage


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True, verbose_name=_("Profile Picture"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    phone = models.CharField(max_length=14, unique=True, primary_key=True, verbose_name=_('Phone Number'))
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified"))
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ["first_name", "last_name","email"]

    objects = UserManager()

    def __str__(self):
        return self.phone

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)