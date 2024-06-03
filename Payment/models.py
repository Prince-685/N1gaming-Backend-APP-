from django.db import models
from django.core.validators import MaxValueValidator
from API.models import CustomUsers

# Create your models here.
class PaymentQRUPI(models.Model):
    image = models.CharField(max_length=255)
    upi_id = models.CharField(max_length=25)


class PaymentForm(models.Model):

    STATUS_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    amount = models.PositiveIntegerField(validators=[MaxValueValidator(10000)])
    txn_id=models.CharField(max_length=25)
    payment_image = models.CharField(max_length=255)
    payment_method =models.CharField(max_length=50, choices=[
        ('Paytm_UPI', 'Paytm UPI'),
        ('PhonePe_UPI', 'Phonepe UPI'),
        ('GPay_UPI', 'GPay UPI'),
        ('other', 'other')
    ])
    upi_id=models.CharField(max_length=25, blank=True)
    user=models.ForeignKey(CustomUsers, db_column='email', on_delete=models.CASCADE)
    status=models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True)


