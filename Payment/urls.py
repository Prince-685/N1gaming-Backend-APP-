from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload_payment_qr/', PaymentQRUPIAPIView.as_view(), name='Upload Payment QR'),
    path('get_payment_qr', PaymentQRUPIAPIView.as_view(), name='Get Payment QR'),
    path('recharge_request/', PaymentFormAPIView.as_view(), name='recharge_request'),
    path('withdraw_request/', WithdrawalRequestAPIView.as_view(), name='withdraw_request'),
    path('account_history', AccountHistoryAPIView.as_view(), name='account-history'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)