from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TimeEntryModel, TSN, UserGame


@receiver(post_save, sender=TimeEntryModel)
def settle_bets(sender, instance):
        
    try:
        today_date=date.today()
        time=instance.Time
        game_date_time=str(today_date)+" "+time
        
        tsn_instances=TSN.objects.filter(gamedate_time=game_date_time)

        for tsn in tsn_instances:
            win_points=0
            game_play = tsn.user_games.all()
            for game in game_play:
                g_name=game.game_name
                res=getattr(instance,g_name)
                if res==game.number:
                    win_points=win_points+game.Playedpoints*90
            
            tsn.winning=win_points
            tsn.save()
            transaction_instance=tsn.transaction
            user=transaction_instance.cuser
            user.balance=user.balance+win_points
            user.save()
    except TSN.DoesNotExist:
        print("No TSN instances found for the given game date and time.")
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        pass