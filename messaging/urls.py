from . import views
from django.urls import include, path 


app_name = 'messaging'
urlpatterns = [
    path('', views.index, name='inbox'),
    path('outbox',views.outbox, name='outbox'),
    path('message/<int:message_id>',views.readMessage, name='readmessage'),
    path('message/<int:message_id>/delete',views.deleteMessage, name = 'deletemessage'),
]