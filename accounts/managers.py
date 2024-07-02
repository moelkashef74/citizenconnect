from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    def phone_number_validator(self, phone):
        phone_regex = r'^[\d\-\+\(\) ]+$'
        validator = RegexValidator(
            regex=phone_regex,
            message=_("Please enter a valid phone number."),
        )
        validator(phone)
        phone_digits = ''.join(filter(str.isdigit, phone))
        if not 10 <= len(phone_digits) <= 14 or (
                not phone_digits.startswith(('010','011','012')) and not phone_digits.startswith(('+2010', '+2011', '+2012'))):
            raise ValueError(_("Please enter a valid phone number."))

        # Check if the phone number starts with '01'
        if phone.startswith('01'):
            # Prepend '+2' to the phone number
            phone = '+2' + phone

        return phone

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Invalid email"))

    def create_user(self, first_name, last_name, phone, email, password, **extra_fields):
        if not phone:
            raise ValueError(_("A phone number is required"))
        self.phone_number_validator(phone)

        if not first_name:
            raise ValueError(_("The first name is required"))
        if not last_name:
            raise ValueError(_("The last name is required"))
        if not email:
            raise ValueError(_("An email is required"))
        self.email_validator(email)

        phone = self.phone_number_validator(phone)
        user = self.model(first_name=first_name, last_name=last_name, phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is_staff must be True for admin user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is_superuser must be True for admin user"))

        phone = self.phone_number_validator(phone)
        user = self.create_user(first_name, last_name, phone, email, password, **extra_fields)
        user.save(using=self._db)
        return user