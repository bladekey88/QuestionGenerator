from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from .models import Message, User
from django.contrib import messages
from .utils import sendMessage, getSystemID, fileUploadMessage




@login_required
#Inbox
def index(request):
    if request.method == 'POST':

        
        if request.POST.get('allMessages'):
            selected_messages = request.POST.getlist('selected_options')
            message_id = Message.objects.filter(message_id__in=selected_messages)
            for message in message_id:
                message.message_read = True
            Message.objects.bulk_update(message_id,['message_read'])
            messages.success(request, '<b>Success:</b> Selected messages have been marked read')
            return HttpResponseRedirect('/messages/')
        
        elif  request.POST.get('delallMessages'):
            selected_messages = request.POST.getlist('selected_options')
            message_id = Message.objects.filter(message_id__in=selected_messages)
            for message in message_id:
                if message.deleted_by is None:
                    message.deleted_by = request.user
                    message.save()
                else:
                    message.delete()
           
            messages.success(request, '<b>Success:</b> The selected messages have been deleted')
            return HttpResponseRedirect('/messages/')

    else:
        privateMessages = Message.objects.filter(to_id=request.user).exclude(deleted_by=request.user).order_by('-message_date')
        context = {'privateMessages':privateMessages,}
        return render(request,'messaging/inbox.html',context)


@login_required
#Outbox
def outbox(request):
    privateMessages = Message.objects.filter(from_id=request.user).exclude(deleted_by=request.user)
    context = {'privateMessages':privateMessages}
    return render(request,'messaging/outbox.html',context)

    

@login_required
#Read Message
def readMessage(request,message_id):
    privateMessage = get_object_or_404(Message,message_id=message_id)
    if request.user==privateMessage.to_id or request.user==privateMessage.from_id or request.user.is_superuser  or request.user==privateMessage.deleted_by: 
        context = {'privateMessage':privateMessage}
        if request.user==privateMessage.to_id:
            privateMessage.message_read = True
            privateMessage.save()

        return render(request,'messaging/message.html',context)
    else:
        raise  Http404("The message could not been found. It may have been deleted.")



def deleteMessage(request,message_id):
    privateMessage = get_object_or_404(Message,message_id=message_id)
    
    if request.user==privateMessage.to_id or request.user==privateMessage.from_id:
        
        if privateMessage.deleted_by is None:
            privateMessage.deleted_by = request.user
            privateMessage.save()
            messages.info(request, '<b>Success:</b> The message has been deleted')
            return HttpResponseRedirect('/messages/')
        else:
            privateMessage.delete()   

                
            messages.info(request, '<b>Success:</b> The message has been deleted')
            return HttpResponseRedirect('/messages/')
    
    else:
        messages.error(request,'<b>Error</b> You do not have permission to delete this message.')
        return HttpResponseRedirect('/messages/message/' + str(message_id))

    