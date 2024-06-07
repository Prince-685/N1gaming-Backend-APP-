import os
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import PaymentForm, PaymentQRUPI
from .serializers import PaymentQRUPISerializer, PaymentFormSerializer, WithdrawalHistorySerializer

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
            'status': request.data.get('status', '') 
        }

        serializer = PaymentFormSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WithdrawalRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawalHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)