from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

def authenticate_user(email, password):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        if check_password(password,user.password):
            return user
    except User.DoesNotExist:
        pass
    return None
