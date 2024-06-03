from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload_payment_qr/', PaymentQRUPIAPIView.as_view(), name='Upload Payment QR'),
    path('get_payment_qr', PaymentQRUPIAPIView.as_view(), name='Get Payment QR'),
    path('recharge_request/', PaymentFormAPIView.as_view(), name='recharge_request'),
    path('get_recharge_request', PaymentFormAPIView.as_view(), name='Recharge Request')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)