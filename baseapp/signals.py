from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Accessories

User = get_user_model()

# @receiver(pre_delete, sender=User)
# def set_user_deleted(sender, instance, **kwargs):
#     Animal.objects.filter(user=instance).update(user_identifier=f"deletedUser#{instance.id}", user=None)
