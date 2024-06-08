from django.urls import path
from . import views

urlpatterns = [
    path('',views.Admin_login_page),
    path('adminlogin', views.AdminLoginAPIView.as_view(), name='admin-login'),
    # path('admindashboard/',views.Admindashboard, name='dashboard'),
    path('update-password/',views.UpdateAdminPasswordAPIView.as_view(), name='update-password'),
    path('percent/', views.SetPercentAPIView.as_view(), name='percent'),
    path('admindashboard/recharge_request', views.RechargeRequestAPIView.as_view(), name='accept-reject-recharge-request'),
    path('admindashboard/withdraw_request', views.WithdrawRequestAPIView.as_view(), name='accept-reject-withdraw-request'),
    path('withdrawal_history', views.WithDrawalHistoryAPIView.as_view(), name='withdraw-history'),
    path('recharge_history', views.RechargeHistoryAPIView.as_view(), name='recharge-history'),
]