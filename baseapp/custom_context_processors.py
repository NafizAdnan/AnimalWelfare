from notification_app.models import BroadcastNotification
def notifications(request):
    allnotifications = BroadcastNotification.objects.all()
    return {'notifications':allnotifications}

from .models import Notification

def unread_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(recipient=request.user, read=False).count()
        return {'unread_count': unread_count}
    else:
        return {}
