from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    message_id = models.AutoField(db_column='message_id', primary_key = True,)
    from_id =  models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null = False, related_name='from_users')
    to_id = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null = False, related_name='to_users')
    message_subject = models.CharField(max_length=255)
    message_body = models.TextField(blank=False,null=False)
    message_date = models.DateTimeField('Message Date', auto_now_add=True)
    message_read = models.BooleanField('Message Read',blank=False, null =False)
    deleted_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null = True, related_name='deleted_users')
    

    def __str__(self):
        return str(self.message_id)

        
