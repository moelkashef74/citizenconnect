from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("please enter a valid email address"))

    def create_user(self, first_name, last_name, email, id, password, **extra_fields):
        if email:
            email=self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("an email address is required"))
        if not first_name:
            raise ValueError(_("the first name is required"))
        if not last_name:
            raise ValueError(_("the last name is required"))
        user=self.model( first_name=first_name, last_name=last_name,email=email, id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) 
        return user
    
    def create_superuser(self, first_name, last_name, email, id, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be true for admin user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is superuser must be true for admin user"))
        
        user=self.create_user( 
            first_name, last_name, email, id, password, **extra_fields
        )
        user.save(using=self._db)
        return user
    
