from django.shortcuts import render
import datetime as dt
from API.models import CustomUsers, Win_Percent
from API.utils import authenticate_user
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from Payment.serializers import PaymentFormSerializer, WithdrawalHistorySerializer
from Payment.models import PaymentForm, WithdrawalHistory
from .permissions import IsSuperUser
from django.contrib.auth.hashers import check_password



def Admin_login_page(request):
    return render(request,'adminLogin.html')

class AdminLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate_user(email=email, password=password)

        if user is not None:
            if user.is_superuser:
                # User is authenticated
                # Delete any existing token
                Token.objects.get(user=user).delete()
                
                # Generate a new token
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({'message':'Logged in Successfully','token': token.key}, status=status.HTTP_200_OK)
            
            
        else:
            # Authentication failed
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class AdminDashboardAPIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsSuperUser]

#     def get(self,request):


class SetPercentAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]
    def get(self,request):
        try:
            win_pencent_instance=Win_Percent.objects.get(pk=1)
            per=win_pencent_instance.percent
        
        except Win_Percent.DoesNotExist:
            per=0
        return render(request,'bar.html',{'percent':per})
    
    def post(self,request):
        per=request.data.get('percent')
        try:
            percent_instance = Win_Percent.objects.get(pk=1)
            percent_instance.percent = per
            percent_instance.save()
        except Win_Percent.DoesNotExist:
            Win_Percent.objects.create(percent=per)
        return render(request,'bar.html',{'percent':per})



class RechargeRequestAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        pending_payments = PaymentForm.objects.filter(status='pending')
        if pending_payments.exists():
            serializer = PaymentFormSerializer(pending_payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No pending recharge requests'}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        txn_id = request.data.get('txn_id')
        new_status = request.data.get('status')

        if not txn_id or not new_status:
            return Response({'message': 'txn_id and status are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recharge_request = PaymentForm.objects.get(txn_id=txn_id)
            recharge_request.status = new_status
            recharge_request.save()
            return Response({'message': 'Status updated successfully'}, status=status.HTTP_200_OK)
        except PaymentForm.DoesNotExist:
            return Response({'message': 'No request found with this txn_id'}, status=status.HTTP_404_NOT_FOUND)

    

class WithdrawRequestAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self,request):
        pending_withdraw_requests = WithdrawalHistory.objects.filter(status='pending')
        if pending_withdraw_requests.exists():
            serializer = WithdrawalHistorySerializer(pending_withdraw_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No pending recharge requests'}, status=status.HTTP_204_NO_CONTENT) 
        
    def patch(self,request):
        withraw_id = request.data.get('withdrawal_id')
        new_status = request.data.get('status')

        if not withraw_id or not new_status:
            return Response({'message': 'txn_id and status are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            withdraw_request = WithdrawalHistory.objects.get(withdrawal_id=withraw_id)
            withdraw_request.status = new_status
            withdraw_request.save()
            return Response({'message': 'Status updated successfully'}, status=status.HTTP_200_OK)
        except PaymentForm.DoesNotExist:
            return Response({'message': 'No request found with this withdrawal_id'}, status=status.HTTP_404_NOT_FOUND)


class UpdateAdminPasswordAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def patch(self,request):
        token_value=request.headers.get('Authorization')
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        token = Token.objects.get(key=token_value.split(' ')[1])
        user = token.user

        # Check if the provided current password matches the user's actual password
        if check_password(current_password, user.password):
            # Set the new password and save the user object
            user.set_password(new_password)
            user.save()
            return render(request, 'dashboard.html', {'message': 'Password updated successfully'})
        else:
            # Return a response indicating that the current password is incorrect
            return Response({'message': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)
        

class RechargeHistoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        history_payments = PaymentForm.objects.filter(status__in=['approve', 'reject'])
        if history_payments.exists():
            serializer = PaymentFormSerializer(history_payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No recharge history available'}, status=status.HTTP_204_NO_CONTENT)
        
class WithDrawalHistoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        history_payments = WithdrawalHistory.objects.filter(status__in=['approve', 'reject'])
        if history_payments.exists():
            serializer = WithdrawalHistorySerializer(history_payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No recharge history available'}, status=status.HTTP_204_NO_CONTENT)
        
