from . import views
from django.urls import include, path 


app_name = 'worksheet'
urlpatterns = [
    path('q', views.makeWorkSheet, name='worksheet'),
    path('',views.selectQuestion,name="selectQuestion"),
    path('test',views.test,name="test"),
    path('word/',views.word,name="word"),
]
