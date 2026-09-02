from .models import WorkerMessage, Notification


def worker_message_counter(request):

    if not request.user.is_authenticated:
        return {
            'worker_unread_messages_count': 0,
        }

    count = WorkerMessage.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    return {
        'worker_unread_messages_count': count,
    }


def notification_context(request):

    if not request.user.is_authenticated:
        return {
            'unread_notifications': [],
            'unread_notification_count': 0,
        }

    unread_notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).order_by('-created_at')[:5]

    unread_notification_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return {
        'unread_notifications': unread_notifications,
        'unread_notification_count': unread_notification_count,
    }