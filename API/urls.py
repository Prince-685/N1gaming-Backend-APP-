from django.urls import path
from . import views
from .views import (
    UserRegistrationAPIView,
    OTPValidationAPIView,
    ResendOTPAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    ResetPasswordRequestAPIView,
    ResetPasswordOTPValidationAPIView,
    ResetPasswordAPIView,
    UpdatePasswordAPIView,
    ResultAPIView,
    RecentResultAPIView,
    TransactionAPIView,
    UserGameAPIView,
    UserBalanceAPIView,
    getUserusernameAPIView,
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user_register'),
    path('validate-otp/', OTPValidationAPIView.as_view(), name='validate_otp'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='resend_otp'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    path('reset-password/request/', ResetPasswordRequestAPIView.as_view(), name='reset_password_request'),
    path('reset-password/otp-validation/', ResetPasswordOTPValidationAPIView.as_view(), name='reset_password_otp-validate'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('update-password/', UpdatePasswordAPIView.as_view(), name='reset_password'),
    path('get-result', ResultAPIView.as_view(), name='get-result'),
    path('get-recent-result', RecentResultAPIView.as_view(), name='get-recent-result'),
    path('transaction/',TransactionAPIView.as_view(),name='transaction'),
    path('get-usergame',UserGameAPIView.as_view(),name='get-usergame'),
    path('get-balance',UserBalanceAPIView.as_view(),name='get-balance'),
    path('get-username',getUserusernameAPIView.as_view(),name='get-username'),
]