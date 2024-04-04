from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask,CrontabSchedule
import json
class BroadcastNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save,sender=BroadcastNotification)
def notification_handler(sender,instance,created, **kwargs):
    #call group_send function directly to send notification or can create a dynamic task in celery beat
    if created:
        schedule,created = CrontabSchedule.objects.get_or_create(hour=instance.broadcast_on.hour,minute = instance.broadcast_on.minute,day_of_month = instance.broadcast_on.day,month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab = schedule,name = "broadcast-notification-"+str(instance.id),task="notifications_app.tasks.broadcast_notification",args = json.dumps((instance.id,)))
    #if not created:

