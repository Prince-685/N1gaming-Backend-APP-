import os
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import PaymentForm, PaymentQRUPI, WithdrawalHistory
from .serializers import PaymentFormCustomSerializer, PaymentQRUPISerializer, PaymentFormSerializer, WithdrawalHistoryCustomSerializer, WithdrawalHistorySerializer
from itertools import chain

# Create your views here.

class PaymentQRUPIAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
            image = request.FILES.get('image')
            upi_id = request.data.get('upi_id')

            if image is None or upi_id is None:
                return Response({'error': 'Image and UPI ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the image file to MEDIA_ROOT
            filename = image.name.replace(' ', '_')
            file_path = os.path.join('payment_qr_upi', filename)
            path = default_storage.save(file_path, image)
            # Create a new PaymentQRUPI instance with image URL
            payment_qr_upi = PaymentQRUPI.objects.create(image=os.path.join(settings.MEDIA_URL, file_path), upi_id=upi_id)

            # Serialize the created instance
            serializer = PaymentQRUPISerializer(payment_qr_upi)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def get(self, request):
        try:
            latest_entry = PaymentQRUPI.objects.latest('id')  # or 'id' if no timestamp
            serializer = PaymentQRUPISerializer(latest_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PaymentQRUPI.DoesNotExist:
            return Response({"message": "No entries found"}, status=status.HTTP_404_NOT_FOUND)

    
    

class PaymentFormAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        token_value = request.headers.get('Authorization')
        token = Token.objects.get(key=token_value.split(' ')[1])

        payment_image = request.FILES.get('payment_image')

        if payment_image is None:
            return Response({'error': 'Payment image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the image file to MEDIA_ROOT
        filename = payment_image.name.replace(' ', '_')
        file_path = os.path.join('payment_request_upi', filename)
        path = default_storage.save(file_path, payment_image)

        data = {
            'amount':request.data.get('amount'),
            'txn_id': request.data.get('txn_id'),
            'payment_image': os.path.join(settings.MEDIA_URL, file_path),
            'payment_method': request.data.get('payment_method'),
            'upi_id': request.data.get('upi_id',""),
            'user': token.user.pk, 
        }

        serializer = PaymentFormSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WithdrawalRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data=request.data
        user=request.user
        amount=data['amount']
        data['user']=user.pk
        if not user.account_number and  not user.holder_name and not user.ifsc_code and  not user.upi_id:
            return Response({'message':'First add all the Bank Details'}, status=status.HTTP_412_PRECONDITION_FAILED)

        if amount<100:
            return Response({'message':'Minimum withrawal amount should be 100'}, status=status.HTTP_400_BAD_REQUEST)

        elif amount>user.balance:
            return Response({'message':'Insufficient Balance'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WithdrawalHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user.balance=user.balance-data['amount']
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class AccountHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch payment and withdrawal records
        try:
            payment_records = PaymentForm.objects.filter(user=request.user.pk)
            payment_serializer = PaymentFormCustomSerializer(payment_records, many=True)
        except PaymentForm.DoesNotExist:
            return Response({"message":"No Records Found"}, status=status.HTTP_204_NO_CONTENT)
        try:
            withdrawal_records = WithdrawalHistory.objects.filter(user=request.user.pk)
            withdrawal_serializer = WithdrawalHistoryCustomSerializer(withdrawal_records, many=True)
        except WithdrawalHistory.DoesNotExist:
            pass

        # Combine and sort the data
        combined_data = list(chain(payment_serializer.data, withdrawal_serializer.data))
        sorted_combined_data = sorted(combined_data, key=lambda x: x['created_at'], reverse=True)

        return Response(sorted_combined_data, status=status.HTTP_200_OK)