import base64
from zoneinfo import ZoneInfo
from rest_framework import serializers
from .models import PaymentForm, PaymentQRUPI, WithdrawalHistory

class PaymentQRUPISerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentQRUPI
        fields = ['image', 'upi_id']


class PaymentFormSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = PaymentForm
        fields = ['amount', 'txn_id', 'payment_image', 'payment_method', 'upi_id', 'user', 'status', 'created_at']

    def get_created_at(self, obj):
        local_tz = ZoneInfo('Asia/Kolkata')
        created_at_kolkata = obj.created_at.astimezone(local_tz)
        formatted_date = created_at_kolkata.strftime('%Y-%m-%d %I:%M %p')
        return formatted_date

    

class WithdrawalHistorySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = WithdrawalHistory
        fields = ['withdrawal_id', 'amount', 'user', 'status', 'created_at']

    def get_created_at(self, obj):
        local_tz = ZoneInfo('Asia/Kolkata')
        created_at_kolkata = obj.created_at.astimezone(local_tz)
        formatted_date = created_at_kolkata.strftime('%Y-%m-%d %I:%M %p')
        return formatted_date

    

class PaymentFormCustomSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = PaymentForm
        fields = ['txn_id', 'amount', 'status', 'created_at', 'type']

    def get_type(self, obj):
        return 'recharge'
    
    def get_created_at(self, obj):
        local_tz = ZoneInfo('Asia/Kolkata')
        created_at_kolkata = obj.created_at.astimezone(local_tz)
        formatted_date = created_at_kolkata.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date

class WithdrawalHistoryCustomSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model = WithdrawalHistory
        fields = ['withdrawal_id', 'amount', 'status', 'created_at', 'type']

    def get_type(self, obj):
        return 'withdrawal'
    
    def get_created_at(self, obj):
        local_tz = ZoneInfo('Asia/Kolkata')
        created_at_kolkata = obj.created_at.astimezone(local_tz)
        formatted_date = created_at_kolkata.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date
