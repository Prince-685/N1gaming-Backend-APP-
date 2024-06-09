from django.urls import path
from . import views

urlpatterns = [
    path('',views.Admin_login_page),
    path('adminlogin/', views.AdminLoginAPIView.as_view(), name='admin-login'),
    path('dashboard', views.Dashboard_page),
    path('recharge-request', views.RechargeRequest_page),
    path('recharge-history', views.RechargeHistory_page),
    path('withdrawal-request', views.WithdrawalRequest_page),
    path('withdraw-history', views.WithdrawalHistory_page),
    path('set-percent', views.SetPercent_page),
    path('change-password', views.ChangePassword_page),
    # path('admindashboard/',views.Admindashboard, name='dashboard'),
    path('update-password/',views.UpdateAdminPasswordAPIView.as_view(), name='update-password'),
    path('percent/', views.WinPercentAPIView.as_view(), name='percent'),
    path('admindashboard/recharge_request', views.RechargeRequestAPIView.as_view(), name='accept-reject-recharge-request'),
    path('admindashboard/withdraw_request', views.WithdrawRequestAPIView.as_view(), name='accept-reject-withdraw-request'),
    path('withdrawal_history', views.WithDrawalHistoryAPIView.as_view(), name='withdraw-history'),
    path('recharge_history', views.RechargeHistoryAPIView.as_view(), name='recharge-history'),
]