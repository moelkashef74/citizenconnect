from django.urls import path
from .views import RegisterUserView, LoginUserView, PasswordResetRequestView, PasswordResetConfirm, SetNewPasswordView, LogoutUserView, TestAuthView, AdminLoginAPIView, VerifyOTPView, UserUpdateView, ChangePasswordView, LastSolvedReportView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-phone/', VerifyOTPView.as_view(), name='verify-phone'),
    path('login/', LoginUserView.as_view() , name='login'),
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<email>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('admin-login/', AdminLoginAPIView.as_view(), name='login'),
    path('user-update/', UserUpdateView.as_view(), name='update-user'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('last-reports/', LastSolvedReportView.as_view(), name='last_solved_report'),

]
