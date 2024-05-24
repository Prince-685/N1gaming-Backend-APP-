from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Admin must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Admin must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUsers(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50,default=None)
    email = models.EmailField(unique=True, validators=[EmailValidator(message='Enter a valid email address.')])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=6,blank=True)
    otp_resend_count = models.IntegerField(default=0)
    last_otp_send_time= models.CharField(max_length=50,blank=True)
    balance = models.IntegerField(default=0)
    
    #Bank Details
    account_number = models.CharField(max_length=50, blank=True)
    holder_name = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=50, blank=True)
    upi_id = models.CharField(max_length=50, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

      # Add related_name arguments to avoid clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.email


class DateModel(models.Model):
    date = models.DateField()

class TimeEntryModel(models.Model):
    date = models.ForeignKey(DateModel, related_name='time_entries', on_delete=models.CASCADE)
    Time = models.CharField(max_length=10)
    A = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    B = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    C = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    D = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    E = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    F = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    G = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    H = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    I = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    J = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    K = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    L = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    M = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    N = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    O = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    P = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    Q = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    R = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    S = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    T = models.CharField(max_length=2, validators=[MinLengthValidator(2)])

    def __str__(self):
        return f"{self.date.date} - {self.Time}"
    
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=25, primary_key=True)  # Assuming transaction_id is a string
    cuser = models.ForeignKey(CustomUsers, related_name="transaction", on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.transaction_id} - {self.date} - {self.cuser.email}"

class TSN(models.Model):
    transaction = models.ForeignKey(Transaction, related_name="tsn", on_delete=models.CASCADE)
    tsn_id = models.CharField(max_length=25, primary_key=True)  # Assuming TSN_id is a string
    gamedate_time = models.CharField(max_length=50)
    playedpoints = models.IntegerField()
    slipdatetime = models.CharField(max_length=50)
    winning = models.CharField(max_length=10,default='live')

    def __str__(self):
        return f"Transaction {self.transaction.transaction_id} - TSN {self.tsn_id} - {self.gamedate_time}"

    class Meta:
        ordering = ['gamedate_time']


class UserGame(models.Model):
    tsn = models.ForeignKey(TSN, on_delete=models.CASCADE, related_name='user_games')
    game_name = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
                                                        ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'),
                                                        ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'),
                                                        ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T')])
    number = models.CharField(max_length=2)
    Playedpoints = models.IntegerField()

    def __str__(self):
        return f"tsn_id:{self.tsn.pk} GameDate_Time: {self.tsn.gamedate_time}, Game: {self.game_name}, Number: {self.number}, Points: {self.Playedpoints}"
    

class Win_Percent(models.Model):
    pid=models.AutoField(primary_key=True)
    percent=models.IntegerField(default=80)

    def __str__(self):

        return f"{self.percent}"