from datetime import date, datetime, timedelta
import random
import time
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import TSN, CustomUsers, DateModel, TimeEntryModel, Transaction, UserGame
from django.core.mail import send_mail
from .serializers import CustomUserSerializer, DateModelSerializer, TSNSerializer, TimeEntrySerializer, TransactionSerializer, UserGameSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .utils import authenticate_user
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound

# Create your views here.
def send_otp(email):

    otp = ''.join(random.choices('0123456789', k=6))
    subject = 'OTP for Email Verification'
    message = f'Your OTP is: {otp}'
    from_email = 'pagalno351@gmail.com'  # Your email address
    to_email = email
    send_mail(subject, message, from_email, [to_email])
    return otp

def generate_unique_id():
    # Get the current timestamp
    timestamp = str(int(time.time()))

   
    id_start = 'B102KMT'
    random_value = str(random.randint(0, 9999))
    # Combine timestamp and additional info and random value
    combined_data = id_start + timestamp + random_value

    

    return combined_data


class UserRegistrationAPIView(APIView):
    def post(self, request):
        data=request.data
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            otp=send_otp(request.data['email'])
            user = serializer.save(otp=otp,last_otp_send_time=datetime.now())
            # Return user data with success message
            return Response({'message': 'OTP sent successfully', 'user_email': user.email}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OTPValidationAPIView(APIView):
    def post(self, request):
        data = request.data
        user_email = data.get('email')
        otp_entered = data.get('otp')

        # Retrieve user instance by ID
        user = get_object_or_404(CustomUsers, email=user_email)
        # Compare entered OTP with stored OTP
        if otp_entered == user.otp:
            # Clear OTP field if OTP is valid
            user.otp = ''
            user.is_active=True
            user.save()
            # Generate authentication token    
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'OTP validation successful', 'token': token.key}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
class ResendOTPAPIView(APIView):
    def post(self, request):
        user_email = request.data.get('email')

        # Retrieve user instance by email
        user = get_object_or_404(CustomUsers, email=user_email)

        resend_limit = 5

        if user.otp_resend_count >= resend_limit:
            # Check if cooldown period has passed
            last_otp_send_time = user.last_otp_send_time.split(".")[0]
            cooldown_end_time = datetime.strptime(last_otp_send_time, "%Y-%m-%d %H:%M:%S")
            cooldown_end_time+=timedelta(hours=24)

            if datetime.now().replace(microsecond=0) < cooldown_end_time:
                # Return error response indicating resend time period
                resend_time_remaining = cooldown_end_time - datetime.now().replace(microsecond=0)
                return Response({'message': f'You have exceeded the resend limit. Please try again after {resend_time_remaining}.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            # Reset resend count and update last resend time
            user.otp_resend_count = 0
            user.last_otp_send_time = datetime.now()
        
        # Generate new OTP
        new_otp = send_otp(user_email)

        # Update user's OTP in the database
        user.otp = new_otp
        user.otp_resend_count += 1
        user.last_otp_send_time= datetime.now()
        user.save()
        
        return Response({'message': 'New OTP sent successfully'}, status=status.HTTP_200_OK)

class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate_user(email=email, password=password)

        if user is not None:
            if user.is_active==True:
                # User is authenticated, generate token
                token = Token.objects.create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
               return Response({'message': 'OTP required', 'email': email}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Authentication failed
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView):
    def post(self, request):
        # Get the user's token value from the request headers
        token_value = request.headers.get('Authorization')

        if token_value:
            # Retrieve the token object associated with the token value
            try:
                token = Token.objects.get(key=token_value.split(' ')[1])
                user = token.user
                
                # Delete the retrieved token
                token.delete()

                # Optionally, you may want to log the user out of all devices by invalidating all of their tokens
                # Here, we're simply deleting all of the user's tokens
                Token.objects.filter(user=user).delete()

                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                pass

        return Response({'message': 'Token not provided or invalid'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordRequestAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUsers, email=email)

        # Generate password reset token
        token = default_token_generator.make_token(user)

        # Send email with password reset link containing the token
        subject = 'Password Reset'
        message = f'Click the following link to reset your password: http://localhost:8000/reset-password/{token}'
        send_mail(subject, message, None, [email])

        return Response({'message': 'Password reset link sent successfully'}, status=status.HTTP_200_OK)


class VerifyTokenAPIView(APIView):
    def get(self,request):
        token = request.GET.get('token')
        try:
            user = CustomUsers.objects.get(pk=default_token_generator.check_token(token))
            if user is not None:
                return Response({'message':'Email Verified Successfully','token':token},status=status.HTTP_200_OK)
        except CustomUsers.DoesNotExist:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # token_value=request.headers.get('Autorization')
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        user = request.user  # Get the authenticated user from the request

        # Check if the provided current password matches the user's actual password
        if check_password(current_password, user.password):
            # Set the new password and save the user object
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        else:
            # Return a response indicating that the current password is incorrect
            return Response({'message': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)
        


class ResultAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            request_date = request.data.get('date', str(date.today()))
            date_instance = DateModel.objects.get(date=request_date)

            # METHOD-1
            
            # time_entries = TimeEntryModel.objects.filter(date=date_instance)
            # serializer = TimeEntrySerializer(time_entries, many=True)

            #METHOD-2
            time_entry=date_instance.time_entries.all()
            serializer = TimeEntrySerializer(time_entry, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DateModel.DoesNotExist:
            raise NotFound("Date not found.")
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RecentResultAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_date = date.today()
            date_instance = DateModel.objects.get(date=current_date)

            current_time = datetime.now()
            recent_minute = current_time.minute // 15 * 15
            recent_time_str = current_time.replace(minute=recent_minute).strftime("%I:%M %p")

            time_instance = TimeEntryModel.objects.get(date=date_instance, Time=recent_time_str)
            serializer = TimeEntrySerializer(time_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DateModel.DoesNotExist:
            raise NotFound("Date not found.")
        except TimeEntryModel.DoesNotExist:
            raise NotFound("Time entry not found.")
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class TransactionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        token_value = request.headers.get('Authorization')
        token = Token.objects.get(key=token_value.split(' ')[1])
        user = token.user
        gamedate_times = data.get('gamedate_times', [])

        if not gamedate_times:
            return Response({'error': 'Select Gametime'}, status=status.HTTP_400_BAD_REQUEST)

        if user.balance < data.get('total_amount'):
            return Response({'message':'Insufficient Balance'}, status=status.HTTP_403_FORBIDDEN)

        transaction_data = {
            'transaction_id': data.get('transaction_id'),
            'date': date.today(),
            'cuser': user.pk,
                            }

        transaction_serializer = TransactionSerializer(data=transaction_data)
        transaction_serializer.is_valid(raise_exception=True)
        transaction_instance = transaction_serializer.save()
        for gamedate_time in gamedate_times:
            t_id = generate_unique_id()
            tsn_data = {
                'transaction': transaction_instance.pk,
                'tsn_id': t_id,
                'gamedate_time': gamedate_time,
                'playedpoints': data.get('points'),
                'slipdatetime': data.get('slipdate_time'),
            }
            tsn_serializer = TSNSerializer(data=tsn_data)
            tsn_serializer.is_valid(raise_exception=True)
            tsn_instance = tsn_serializer.save()

            for user_game_data in data.get('GamePlay', []):
                usergame_data = {
                    'tsn': tsn_instance.pk,
                    'game_name': user_game_data[0],
                    'number': user_game_data[2:4],
                    'Playedpoints': user_game_data[7:],
                }
                usergame_serializer = UserGameSerializer(data=usergame_data)
                usergame_serializer.is_valid(raise_exception=True)
                usergame_serializer.save()

        user.balance -= data.get('total_amount')
        user.save()

        return Response({'success': 'Data saved successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        requested_date = request.data.get('date', date.today())
        token_value = request.headers.get('Authorization')
        token = Token.objects.get(key=token_value.split(' ')[1])
        user = token.user

        transaction_instance = Transaction.objects.filter(cuser=user.pk, date=requested_date).order_by('-date')[:20]
        response_data = []

        for transaction in transaction_instance:
            tsn_instance = TSN.objects.filter(transaction=transaction.pk).order_by('-gamedate_time')[:20]
            tsns_data = TSNSerializer(tsn_instance, many=True).data

            extracted_tsns_data = []
            for tsn_data in tsns_data:
                extracted_tsn_data = {
                    "tsn_id": tsn_data.get("tsn_id", ""),
                    "gamedate_time": tsn_data.get("gamedate_time", ""),
                    "playedpoints": tsn_data.get("playedpoints", ""),
                    "slipdatetime": tsn_data.get("slipdatetime", ""),
                }
                extracted_tsns_data.append(extracted_tsn_data)

            transaction_data = {
                "transaction_id": transaction.transaction_id,
                "tsns": extracted_tsns_data,
            }

            response_data.append(transaction_data)

        return Response({'transactionList': response_data}, status=status.HTTP_200_OK)

class UserGameAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tsn_id = request.data.get('tsn_id') 
            if not tsn_id:
                return Response({"error": "tsn_id parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
            
            tsn_instance = get_object_or_404(TSN, tsn_id=tsn_id)
            user_games = tsn_instance.user_games.all()
            serializer = UserGameSerializer(user_games, many=True)
            response_data=[]
            for usergame in serializer.data:
                usergame_data={
                    "game_name":usergame.get('game_name'),
                    "number":usergame.get('number'),
                    "Playedpoints":usergame.get('Playedpoints')
                }
                response_data.append(usergame_data)
            response_data={
                'tsn_id':tsn_id,
                'usergame':response_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
        except TSN.DoesNotExist:
            return Response({"error": "TSN with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class UserBalanceAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            token_value = request.headers.get('Authorization')
            token = Token.objects.get(key=token_value.split(' ')[1])
            user = token.user
            balance=user.balance
            return Response({'balance':balance},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
