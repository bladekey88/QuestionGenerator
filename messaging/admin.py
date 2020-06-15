from django.contrib import admin

from .models import Message


admin.site.empty_value_display = '(None)'


class MessageAdmin(admin.ModelAdmin):

   
    list_display = ('message_id','from_id', 'to_id', 'message_subject', 'message_read','message_date' )
    search_fields = ['from_id', 'to_id', 'message_subject']
    list_filter  = ['from_id', 'to_id','message_read', 'message_date']
    readonly_fields = ('message_id', 'deleted_by', 'message_read' )  
    ordering = ['message_id']


admin.site.register(Message, MessageAdmin)