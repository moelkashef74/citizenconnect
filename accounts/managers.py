from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))

    def phone_number_validator(self, phone_number):
        phone_number_regex = r'^[\d\-\+\(\) ]+$'
        validator = RegexValidator(
            regex=phone_number_regex,
            message=_("Please enter a valid phone number."),
        )
        validator(phone_number)
        phone_number_digits = ''.join(filter(str.isdigit, phone_number))
        if len(phone_number_digits) not in (10, 11):
            raise ValueError(_("Please enter a valid phone number."))

    def create_user(self, first_name, last_name, email_or_phone, id, password, **extra_fields):
        if email_or_phone:
            if '@' in email_or_phone:
                email = email_or_phone
                self.email_validator(email)
            else:
                phone_number = email_or_phone
                self.phone_number_validator(phone_number)
        else:
            raise ValueError(_("An email address or phone number is required"))
            
        if not first_name:
            raise ValueError(_("The first name is required"))
        if not last_name:
            raise ValueError(_("The last name is required"))
        
        user = self.model(first_name=first_name, last_name=last_name, email_or_phone=email_or_phone, id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email_or_phone, id, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
     #   extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is_staff must be True for admin user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is_superuser must be True for admin user"))
        
        user = self.create_user(first_name, last_name, email_or_phone, id, password, **extra_fields)
        user.save(using=self._db)
        return user
