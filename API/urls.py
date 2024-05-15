from django.urls import path
from .views import (
    UserRegistrationAPIView,
    OTPValidationAPIView,
    ResendOTPAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    ResetPasswordRequestAPIView,
    VerifyTokenAPIView,
    UpdatePasswordAPIView,
    ResultAPIView,
    RecentResultAPIView,
    TransactionAPIView,
    UserGameAPIView,
    UserBalanceAPIView,
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user_register'),
    path('validate-otp/', OTPValidationAPIView.as_view(), name='validate_otp'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='resend_otp'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    path('reset-password/request/', ResetPasswordRequestAPIView.as_view(), name='reset_password_request'),
    path('verify-token', VerifyTokenAPIView.as_view(), name='verify-token'),
    path('update-password/', UpdatePasswordAPIView.as_view(), name='reset_password'),
    path('get-result', ResultAPIView.as_view(), name='get-result'),
    path('get-recent-result', RecentResultAPIView.as_view(), name='get-recent-result'),
    path('transaction/',TransactionAPIView.as_view(),name='transaction'),
    path('get-usergame',UserGameAPIView.as_view(),name='get-usergame'),
    path('get-balance',UserBalanceAPIView.as_view(),name='get-balance'),
]
