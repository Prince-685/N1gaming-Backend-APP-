from django.urls import path
from . import views

urlpatterns = [
    path('',views.Admin_login_page),
    # path('admindashboard/',views.Admindashboard, name='dashboard'),
    path('feedresult/',views.FeedResult),
    path('adduser/',views.AddUser),
    path('changePass',views.Admin_pass_change_page),
    path('updateCreditpage',views.Update_Credit),
    path('setbar/',views.Set_Bar),
   
]