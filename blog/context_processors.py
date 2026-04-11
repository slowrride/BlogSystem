def unread_count(request):
    """
    上下文处理器：为所有模板提供未读通知数量和未读消息数量
    """
    if request.user.is_authenticated:
        unread_notification_count = request.user.notifications.filter(is_read=False).count()
        unread_message_count = request.user.received_messages.filter(is_read=False).count()
    else:
        unread_notification_count = 0
        unread_message_count = 0
    return {
        'unread_count': unread_notification_count,
        'unread_message_count': unread_message_count
    }
