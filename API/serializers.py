from rest_framework import serializers
from .models import TSN, CustomUsers, DateModel, TimeEntryModel, Transaction, UserGame

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUsers.objects.create_user(**validated_data)
        return user

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUsers.objects.create_admin(**validated_data)
        return user


class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntryModel
        exclude = ['id', 'date']
        

class DateModelSerializer(serializers.ModelSerializer):
    time_data = TimeEntrySerializer(many=True, read_only=True)

    class Meta:
        model = DateModel
        fields = ['date', 'time_data']


class TransactionSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'date', 'cuser']

    
class TSNSerializer(serializers.ModelSerializer):

    class Meta:
        model = TSN
        fields = ['transaction', 'tsn_id', 'gamedate_time', 'playedpoints', 'slipdatetime']



class UserGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGame
        fields = ['tsn', 'game_name', 'number', 'Playedpoints']

