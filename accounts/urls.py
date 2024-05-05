from django.urls import path
from .views import RegisterUserView, LoginUserView, PasswordResetRequestView, PasswordResetConfirm, SetNewPasswordView, LogoutUserView, TestAuthView, AdminLoginView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view() , name='login'),
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
]
