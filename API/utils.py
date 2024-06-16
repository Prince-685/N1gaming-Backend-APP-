from datetime import datetime
import random,time
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.template import loader
from django.template.loader import render_to_string


def authenticate_user(email, password):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        if check_password(password,user.password):
            return user
    except User.DoesNotExist:
        pass
    return None


def send_otp(email,subject,html_message):

    otp = ''.join(random.choices('0123456789', k=6))
    message = f'Your OTP is: {otp}'
    from_email = 'pagalno351@gmail.com'  # Your email address
    to_email = email
    send_mail(subject, message, from_email, [to_email], html_message=html_message)
    return otp

def handle_otp_for_user(user, email):
                html_message=email_confirmation_message(email)
                subject="Registration Verification"
                otp = send_otp(email,subject,html_message)
                user.otp = otp
                user.last_otp_send_time = datetime.now()
                user.save()

def email_confirmation_message(to_email):
    otp = ''.join(random.choices('0123456789', k=6))
    context = {
        'email': to_email,
        'timestamp': datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
        'confirmation_code': otp,
    }
    
    return loader.render_to_string('email-confirmation.html', context)

def reset_password_message(to_email,subject):
    otp = ''.join(random.choices('0123456789', k=6))
    context = {
        'email': to_email,
        'timestamp': datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
        'confirmation_code': otp,
    }
    message = render_to_string("forget-password.html", context)
    send_mail(subject, '', 'pagalno351@gmail.com', [to_email], html_message=message)
    return otp

def generate_unique_id():
    # Get the current timestamp
    timestamp = str(int(time.time()))
   
    id_start = 'B102KMT'
    random_value = str(random.randint(0, 9999))
    # Combine timestamp and additional info and random value
    combined_data = id_start + timestamp + random_value

    return combined_data



def wining_result(sold_ticket,percent):
    result={}
    game_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    random_slot_list=[]
    for i in game_names:
        playedpoint=sold_ticket[i].values()
        numbers=sold_ticket[i].keys()
        max_win=sum(playedpoint)*percent/100
        if max_win>=min(sold_ticket[i].values())*90:
            mul_playedpoint=list(np.array(list(playedpoint)) * 90)
            closest_index = min((i for i, value in enumerate(mul_playedpoint) if value <= max_win), default=None, key=lambda i: max_win - mul_playedpoint[i])
            result[i]=list(numbers)[closest_index]
        else:
            random_slot_list.append(i)
    remaining_sum=0
    for i in random_slot_list:
        remaining_sum+=sum(sold_ticket[i].values())
    print(remaining_sum)
    max_am=remaining_sum*percent/100
    print(random_slot_list)
    win_slot=random.choice(random_slot_list)
    print(win_slot)
    print(max_am)
    for i in random_slot_list:
        numbers=sold_ticket[i].keys()
        if i==win_slot:
            playedpoint=sold_ticket[i].values()
            mul_playedpoint=list(np.array(list(playedpoint)) * 90)
            closest_index = min((i for i, value in enumerate(mul_playedpoint) if value <= max_am), default=None, key=lambda i: max_am - mul_playedpoint[i])
            if closest_index==None:
                generated_number=-1
                while(True):
                    generated_number=random.randint(0, 99)
                    generated_number="{:02d}".format(generated_number)
                    if(generated_number not in numbers):
                        result[i]=generated_number
                        break
            else:
                result[i]=list(numbers)[closest_index]
        else:
            generated_number=-1
            while(True):
                generated_number=random.randint(0, 99)
                generated_number="{:02d}".format(generated_number)
                if(generated_number not in numbers):
                    result[i]=generated_number
                    break
            
    return result
