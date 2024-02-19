from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
# import random
# from django.core.mail import EmailMessage
# #from .models import User, OneTimePassword
# from django.conf import settings


# def generateOtp():
#     otp=""
#     for i in range(6):
#         otp += str(random.randint(1, 9))
#     return otp


# def send_code_to_user(email):
#     subject="One time passcode for email verification"
#     otp_code=generateOtp()
#     print(otp_code)
#     user=User.objects.get(email=email)
#     current_site="myAuth.com"
#     email_body= f"Hi {user.first_name} thanks for signing up on {current_site} pleasw verify your email with the \n one time passcode {otp_code}"
#     from_email=settings.DEFAULT_FORM_EMAIL

#     OneTimePassword.objects.create(user=user, code= otp_code)

#     d_email=EmailMessage(subject=subject, body= email_body, from_email=from_email, to=[email])
#     d_email.send(fail_silently=True)


def send_normal_email(data):
    message = Mail(
        from_email='citizenconnect@mail.com',
        to_emails=data['to_email'],
        subject=data['email_subject'],
        plain_text_content=data['email_body'])

    try:
        sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

