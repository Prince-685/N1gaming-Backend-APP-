from django.shortcuts import render
from datetime import date
from API.models import TSN, CustomUsers, Transaction, Win_Percent
from API.utils import authenticate_user
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from API.serializers import BankDetailSerializer
from Payment.serializers import PaymentFormSerializer, WithdrawalHistorySerializer
from Payment.models import PaymentForm, WithdrawalHistory
from .permissions import IsSuperUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils.dateparse import parse_date



def Admin_login_page(request):
    return render(request,'adminLogin.html')


@login_required
def Dashboard_page(request):
    return render(request, 'dashboard.html')


@login_required
def PaymentQR_page(request):
    return render(request, 'paymentQR.html')

@login_required
def RechargeRequest_page(request):
    return render(request, 'RechargeRequest.html')


@login_required
def RechargeHistory_page(request):
    return render(request, 'RechargeHistory.html')


@login_required
def WithdrawalRequest_page(request):
    return render(request, 'WithdrawalRequest.html')


@login_required
def WithdrawalHistory_page(request):
    return render(request, 'WithdrawHistory.html')


@login_required
def SetPercent_page(request):
    return render(request, 'bar.html')


@login_required
def ChangePassword_page(request):
    return render(request, 'passAdmin.html')


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
                login(request, user)
                return Response({'message':'Logged in Successfully','token': token.key}, status=status.HTTP_200_OK)            
        else:
            # Authentication failed
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class AdminDashboardDataAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]
    def get(self,request):

        today_bets,today_bet_loss,today_bets_won,today_profit=0,0,0,0
        overall_bets,overall_bet_loss,overall_bets_won,overall_profit=0,0,0,0
        try:
            tsn_instance=TSN.objects.all()
            for item in tsn_instance:
                if item.transaction.date==date.today():
                    today_bets+=int(item.playedpoints)
                    if item.winning=='live':
                        continue
                    elif int(item.winning)>0:
                        today_bets_won+=int(item.winning)
                    else:
                        today_bet_loss+=int(item.playedpoints)
                else:
                    overall_bets+=int(item.playedpoints)
                    if item.winning=='live':
                        continue
                    elif int(item.winning)>0:
                        overall_bets_won+=int(item.winning)
                    else:
                        overall_bet_loss+=int(item.playedpoints)

            today_profit=today_bets-today_bets_won
            overall_bets+=today_bets
            overall_bet_loss+=today_bet_loss
            overall_bets_won+=today_bets_won
            overall_profit=overall_bets-overall_bets_won
            response_data = {
                "today_bets": today_bets,
                "today_bet_loss": today_bet_loss,
                "today_bets_won": today_bets_won,
                "today_profit": today_profit,
                "overall_bets": overall_bets,
                "overall_bet_loss": overall_bet_loss,
                "overall_bets_won": overall_bets_won,
                "overall_profit": overall_profit,
            }

            return Response(response_data,status=status.HTTP_200_OK)

        except TSN.DoesNotExist:
            context = {
                "today_bets": today_bets,
                "today_bet_loss": today_bet_loss,
                "today_bets_won": today_bets_won,
                "today_profit": today_profit,
                "overall_bets": overall_bets,
                "overall_bet_loss": overall_bet_loss,
                "overall_bets_won": overall_bets_won,
                "overall_profit": overall_profit,
            }
            return render(request, "dashboard.html",context,status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class UserListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        try:
            users = CustomUsers.objects.filter(is_superuser=False)
            users=users.order_by('-date_joined')
            response_data=[]
            for user in users:
                today_bets,today_winning,overall_bets,overall_winning=0,0,0,0
                try:

                    tsn_data=TSN.objects.filter(transaction__cuser=user)
                    for item in tsn_data:
                        if item.transaction.date==date.today():
                            if item.winning=='live':
                                today_bets+=int(item.playedpoints)
                            else:
                                today_bets+=int(item.playedpoints)
                                today_winning+=int(item.winning)
                        else:
                            if item.winning=='live':
                                overall_bets+=int(item.playedpoints)
                            else:
                                overall_bets+=int(item.playedpoints)
                                overall_winning+=int(item.winning)
                    overall_bets+=int(today_bets)
                    overall_winning+=int(today_winning)
                    
                except Transaction.DoesNotExist:
                    pass

                user_data={
                        'user':user.email,
                        'today_bets':today_bets,
                        'today_winning':today_winning,
                        'overall_bets':overall_bets,
                        'overall_winning':overall_winning,
                        'date_joined':user.date_joined,
                        'status':'Active' if user.is_active else 'Pending'
                    }
                response_data.append(user_data)
            return Response(response_data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RechargeRequestAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        pending_payments = PaymentForm.objects.filter(status='pending')
        if pending_payments.exists():
            serializer = PaymentFormSerializer(pending_payments, many=True)
            modified_data = []
            for payment in serializer.data:
                user = CustomUsers.objects.get(pk=payment['user'])
                payment['user']=user.email
                modified_data.append(payment)
            return Response(modified_data, status=status.HTTP_200_OK)
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
            response_data = []
            for withdraw_request in pending_withdraw_requests:
                withdraw_data = WithdrawalHistorySerializer(withdraw_request).data
                user_id = withdraw_data['user']
                try:
                    user = CustomUsers.objects.get(id=user_id)
                    bank_detail = BankDetailSerializer(user).data
                    withdraw_data['bank_details'] = bank_detail
                    withdraw_data['user']=user.email
                except CustomUsers.DoesNotExist:
                    withdraw_data['bank_details'] = None
                response_data.append(withdraw_data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No pending recharge requests'}, status=status.HTTP_204_NO_CONTENT) 
        
    def patch(self,request):
        withraw_id = request.data.get('withdrawal_id')
        new_status = request.data.get('status')

        if not withraw_id or not new_status:
            return Response({'message': 'withdraw_id and status are required'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        else:
            # Return a response indicating that the current password is incorrect
            return Response({'message': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)
        

class RechargeHistoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        date_param = request.query_params.get('date')
        history_payments = PaymentForm.objects.filter(status__in=['approve', 'reject'])

        if history_payments.exists():
            if date_param:
                try:
                    filter_date = parse_date(date_param)
                    history_payments = history_payments.filter(created_at__date=filter_date)
                except ValueError:
                    return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
            history_payments = history_payments.order_by('-created_at')
            serializer = PaymentFormSerializer(history_payments, many=True)
            modified_data = []
            for payment in serializer.data:
                user = CustomUsers.objects.get(pk=payment['user'])
                payment['user']=user.email
                # Exclude 'payment_image' from payment data
                payment.pop('payment_image', None)
                modified_data.append(payment)
            return Response(modified_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No recharge history available'}, status=status.HTTP_204_NO_CONTENT)
        
class WithDrawalHistoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        date_param = request.query_params.get('date')
        history_payments = WithdrawalHistory.objects.filter(status__in=['approve', 'reject'])

        if date_param:
            try:
                filter_date = parse_date(date_param)
                history_payments = history_payments.filter(created_at__date=filter_date)
            except ValueError:
                return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        history_payments = history_payments.order_by('-created_at')

        if history_payments.exists():
            serializer = WithdrawalHistorySerializer(history_payments, many=True)
            modified_data = []
            for payment in serializer.data:
                user = CustomUsers.objects.get(pk=payment['user'])
                payment['user']=user.email
                modified_data.append(payment)
            return Response(modified_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No recharge history available'}, status=status.HTTP_204_NO_CONTENT)
        

class WinPercentAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        try:
            instance= Win_Percent.objects.get(pk=1)
            return Response({'percent': instance.percent}, status=status.HTTP_200_OK)
        except Win_Percent.DoesNotExist:
            percent=0
            return Response({'percent':percent}, status=status.HTTP_200_OK)
        
    def post(self, request):
        percent=request.data.get('percent')
        try:
            instance= Win_Percent.objects.get(pk=1)
            instance.percent=percent
            instance.save()
            return Response({'percent': instance.percent,"message":"Win percentage set Successfully"}, status=status.HTTP_200_OK)
        except Win_Percent.DoesNotExist:
            Win_Percent.objects.create(percent=percent)
            return Response({'percent': instance.percent,"message":"Win percentage set Successfully"}, status=status.HTTP_201_CREATED)
