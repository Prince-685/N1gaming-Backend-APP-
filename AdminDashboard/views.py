from django.shortcuts import render
import datetime as dt
from API.models import CustomUsers, Win_Percent


# def Admindashboard(request):
#     today=dt.date.today()
#     user_instance=CustomUsers.objects.all()
#     user_detail=[]
#     for user in user_instance:
#       l=[]
#       account_instance=model.Account.objects.filter(user=user,date=today)
#       playedpoints=sum([entry.play_points for entry in account_instance])
#       earnpoints=sum([entry.earn_points for entry in account_instance])
#       endpoint=playedpoints-earnpoints
#       profit=playedpoints*8/100
#       net_profit=endpoint-profit
#       l.append(user.username)
#       l.append(playedpoints)
#       l.append(earnpoints)
#       l.append(endpoint)
#       l.append(profit)
#       l.append(net_profit)
#       user_detail.append(l)
#     account_instance=model.Account.objects.filter(date=today)
#     totalplayedpoints=sum([entry.play_points for entry in account_instance])
#     totalearnpoints=sum([entry.earn_points for entry in account_instance])
#     endpoints=sum([entry.end_points for entry in account_instance])
#     totalprofit=sum([entry.net_profit for entry in account_instance])

#     return render(request,'dashboard.html',{'playedpoint':totalplayedpoints,'earnpoint':totalearnpoints,'endpoint':endpoints,'profit':totalprofit,'userdata':user_detail})

def AddUser(request):
    return render(request,'AddUser.html')

def FeedResult(request):
    return render(request,'Result.html')

def Admin_login_page(request):
    return render(request,'adminLogin.html')

def Admin_pass_change_page(request):
    return render(request,'passAdmin.html')

def Update_Credit(request):
    if request.method=='POST':

        username=request.POST.get('data_username')
        credit=request.POST.get('data_credit')
    
    li=[username,credit]
    return render(request,'UpdateCredit.html',{'row':li})

def Set_Bar(request):
    win_pencent_instance=Win_Percent.objects.get(pk=1)
    per=win_pencent_instance.percent
    return render(request,'bar.html',{'percent':per})

