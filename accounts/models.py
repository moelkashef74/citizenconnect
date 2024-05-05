from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group



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
    


class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name=_("Username"))
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="admin_user_permissions",
    )
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="admin_groups",
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = (
            ("can_view_admin", "Can view admin"),  # renamed permission
        )

    def __str__(self):
        return self.username