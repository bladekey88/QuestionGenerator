from .models import Message



def unreadMessages(request):
    if request.user.is_anonymous == False:
        unread_messages = Message.objects.filter(to_id=request.user,message_read=0).exclude(deleted_by=request.user).count()
        return {
            'unread_messages': unread_messages
        }
    else:
        return {
            'unread_messages' : None
        }