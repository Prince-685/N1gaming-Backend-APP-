
from datetime import datetime,date, timedelta
import random
from time import strptime

from .utils import wining_result
from .models import DateModel,TimeEntryModel,Transaction,TSN,UserGame,Win_Percent


def Save_result():
    
    win_percent_instance=Win_Percent.objects.first()
    given_win_p=win_percent_instance.percent
    time_str = datetime.now().replace(second=0, microsecond=0).time()
    today=date.today()


    game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    ticket_sold={}
    if TSN.objects.filter(gamedate_time=time_str).exists():
        for game_name in game_names:
            n=[]
            p=[]
            tp=[]
            Tsn_instance=TSN.objects.filter(gamedate_time=time_str)
            for t in Tsn_instance:

                gplay =t.user_games.all()
                if gplay.exists():
                    numbers = [entry.number for entry in gplay]
                    playedpoint = [entry.Playedpoints for entry in gplay]
                    totalplaypoints = sum([entry.Playedpoints for entry in gplay])
                    n.append(numbers)
                    p.append(playedpoint)
                    tp.append(totalplaypoints)
            tppoints=sum(tp)
            if n and p and tppoints:
                number=[]
                points=[]
                for i in range(len(n)):
                    for j in range(len(n[i])):
                        if n[i][j] not in number:
                            
                            number.append(n[i][j])
                            points.append(p[i][j])
                        else:
                            a=number.index(n[i][j])
                            points[a]=points[a]+p[i][j]
                ticket_sold[game_name]=dict(zip(number,points))       
        winresult=wining_result(ticket_sold,given_win_p)
        date_instance, _ = DateModel.objects.get_or_create(date=today)
        time_entry = TimeEntryModel(
                date=date_instance,
                Time=time_str,
                A=winresult['A'],
                B=winresult['B'],
                C=winresult['C'],
                D=winresult['D'],
                E=winresult['E'],
                F=winresult['F'],
                G=winresult['G'],
                H=winresult['H'],
                I=winresult['I'],
                J=winresult['J'],
                K=winresult['K'],
                L=winresult['L'],
                M=winresult['M'],
                N=winresult['N'],
                O=winresult['O'],
                P=winresult['P'],
                Q=winresult['Q'],
                R=winresult['R'],
                S=winresult['S'],
                T=winresult['T'],
            )        
        time_entry.save()
        

    else:
        game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
        result_dict = {}
        for game_name in game_names:
            result_dict[game_name] = f"{random.randint(0, 99):02d}"

        date_instance, _ = DateModel.objects.get_or_create(date=today)
        time_entry = TimeEntryModel(
                date=date_instance,
                Time=time_str,
                A=result_dict['A'],
                B=result_dict['B'],
                C=result_dict['C'],
                D=result_dict['D'],
                E=result_dict['E'],
                F=result_dict['F'],
                G=result_dict['G'],
                H=result_dict['H'],
                I=result_dict['I'],
                J=result_dict['J'],
                K=result_dict['K'],
                L=result_dict['L'],
                M=result_dict['M'],
                N=result_dict['N'],
                O=result_dict['O'],
                P=result_dict['P'],
                Q=result_dict['Q'],
                R=result_dict['R'],
                S=result_dict['S'],
                T=result_dict['T'],
            )        
        time_entry.save()
    


