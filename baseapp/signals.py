from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Animal

User = get_user_model()

@receiver(pre_delete, sender=User)
def set_user_deleted(sender, instance, **kwargs):
    Animal.objects.filter(uploaded_by=instance).update(uploaded_by_identifier=f"deletedUser#{instance.id}", uploaded_by=None)
