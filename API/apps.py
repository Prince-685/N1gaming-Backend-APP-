from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'API'


# from datetime import datetime,date, timedelta
# import random
# from time import strptime
# from .models import DateModel,TimeEntryModel,Transaction,TSN,UserGame,Win_Percent

# def wining_result(sold_ticket,percent):
#     result={}
#     game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
#     random_slot_list=[]
#     for i in game_names:
#         playedpoint=sold_ticket[i].values()
#         numbers=sold_ticket[i].keys()
#         max_win=sum(playedpoint)*percent/100
#         if max_win>=min(sold_ticket[i].values())*90:
#             mul_playedpoint=list(np.array(list(playedpoint)) * 90)
#             closest_index = min((i for i, value in enumerate(mul_playedpoint) if value <= max_win), default=None, key=lambda i: max_win - mul_playedpoint[i])
#             result[i]=list(numbers)[closest_index]
#         else:
#             random_slot_list.append(i)
#     remaining_sum=0
#     for i in random_slot_list:
#         remaining_sum+=sum(sold_ticket[i].values())
#     print(remaining_sum)
#     max_am=remaining_sum*percent/100
#     print(random_slot_list)
#     win_slot=random.choice(random_slot_list)
#     print(win_slot)
#     print(max_am)
#     for i in random_slot_list:
#         numbers=sold_ticket[i].keys()
#         if i==win_slot:
#             playedpoint=sold_ticket[i].values()
#             mul_playedpoint=list(np.array(list(playedpoint)) * 90)
#             closest_index = min((i for i, value in enumerate(mul_playedpoint) if value <= max_am), default=None, key=lambda i: max_am - mul_playedpoint[i])
#             if closest_index==None:
#                 generated_number=-1
#                 while(True):
#                     generated_number=random.randint(0, 99)
#                     generated_number="{:02d}".format(generated_number)
#                     if(generated_number not in numbers):
#                         result[i]=generated_number
#                         break
#             else:
#                 result[i]=list(numbers)[closest_index]
#         else:
#             generated_number=-1
#             while(True):
#                 generated_number=random.randint(0, 99)
#                 generated_number="{:02d}".format(generated_number)
#                 if(generated_number not in numbers):
#                     result[i]=generated_number
#                     break
            
#     return result

# def Save_result():
    
#     win_percent_instance=Win_Percent.objects.first()
#     given_win_p=win_percent_instance.percent
#     time_str = datetime.now().replace(second=0, microsecond=0).time()
#     today=date.today()


#     game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
#     ticket_sold={}
#     if TSN.objects.filter(gamedate_time=time_str).exists():
#         for game_name in game_names:
#             n=[]
#             p=[]
#             tp=[]
#             Tsn_instance=TSN.objects.filter(gamedate_time=time_str)
#             for t in Tsn_instance:

#                 gplay =t.user_games.all()
#                 if gplay.exists():
#                     numbers = [entry.number for entry in gplay]
#                     playedpoint = [entry.Playedpoints for entry in gplay]
#                     totalplaypoints = sum([entry.Playedpoints for entry in gplay])
#                     n.append(numbers)
#                     p.append(playedpoint)
#                     tp.append(totalplaypoints)
#             tppoints=sum(tp)
#             if n and p and tppoints:
#                 number=[]
#                 points=[]
#                 for i in range(len(n)):
#                     for j in range(len(n[i])):
#                         if n[i][j] not in number:
                            
#                             number.append(n[i][j])
#                             points.append(p[i][j])
#                         else:
#                             a=number.index(n[i][j])
#                             points[a]=points[a]+p[i][j]
#                 ticket_sold[game_name]=dict(zip(number,points))       
#         winresult=wining_result(ticket_sold,given_win_p)
#         date_instance, _ = DateModel.objects.get_or_create(date=today)
#         time_entry = TimeEntryModel(
#                 date=date_instance,
#                 Time=time_str,
#                 A=winresult['A'],
#                 B=winresult['B'],
#                 C=winresult['C'],
#                 D=winresult['D'],
#                 E=winresult['E'],
#                 F=winresult['F'],
#                 G=winresult['G'],
#                 H=winresult['H'],
#                 I=winresult['I'],
#                 J=winresult['J'],
#                 K=winresult['K'],
#                 L=winresult['L'],
#                 M=winresult['M'],
#                 N=winresult['N'],
#                 O=winresult['O'],
#                 P=winresult['P'],
#                 Q=winresult['Q'],
#                 R=winresult['R'],
#                 S=winresult['S'],
#                 T=winresult['T'],
#             )        
#         time_entry.save()
        

#     else:
#         game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
#         result_dict = {}
#         for game_name in game_names:
#             result_dict[game_name] = f"{random.randint(0, 99):02d}"

#         date_instance, _ = DateModel.objects.get_or_create(date=today)
#         time_entry = TimeEntryModel(
#                 date=date_instance,
#                 Time=time_str,
#                 A=result_dict['A'],
#                 B=result_dict['B'],
#                 C=result_dict['C'],
#                 D=result_dict['D'],
#                 E=result_dict['E'],
#                 F=result_dict['F'],
#                 G=result_dict['G'],
#                 H=result_dict['H'],
#                 I=result_dict['I'],
#                 J=result_dict['J'],
#                 K=result_dict['K'],
#                 L=result_dict['L'],
#                 M=result_dict['M'],
#                 N=result_dict['N'],
#                 O=result_dict['O'],
#                 P=result_dict['P'],
#                 Q=result_dict['Q'],
#                 R=result_dict['R'],
#                 S=result_dict['S'],
#                 T=result_dict['T'],
#             )        
#         time_entry.save()



# def setlle_bets():
#     current_time = datetime.now()
#     adjusted_time = current_time - timedelta(minutes=2)
#     adjusted_time = adjusted_time.replace(second=0, microsecond=0).time()

    
