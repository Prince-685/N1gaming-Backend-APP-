from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PaymentForm


@receiver(post_save, sender=PaymentForm)
def update_user_balance(sender, instance, created, **kwargs):
    # Check if the instance is being updated (not created)
    if not created:
        # Get the previous value of the status field
        previous_instance = PaymentForm.objects.get(pk=instance.pk)
        previous_status = previous_instance.status

        # Check if the status field value is in either approve or reject
        if instance.status in ['approve', 'reject']:
            if instance.status == 'approve':
                # Add the amount to the user's balance
                user = instance.user
                user.balance += instance.amount
                user.save()
            elif instance.status == 'reject':
                # Do nothing on reject
                pass