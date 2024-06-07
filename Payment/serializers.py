import base64
from rest_framework import serializers
from .models import PaymentForm, PaymentQRUPI, WithdrawalHistory

class PaymentQRUPISerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentQRUPI
        fields = ['image', 'upi_id']


class PaymentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentForm
        fields = ['amount', 'txn_id', 'payment_image', 'payment_method', 'upi_id', 'user', 'status', 'created_at']


class WithdrawalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalHistory
        fields = ['withdrawal_id', 'amount', 'user', 'status', 'created_at']