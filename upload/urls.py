from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import include
# from django.contrib.auth.mixins import LoginRequiredMixin






app_name = 'upload'
urlpatterns = [
    path('', views.index, name='index'),
    
    # ex: /upload/topic
    path('topic/', views.topic, name='topic'),
    # ex: /upload/topic/1
    path('topic/<int:topicid>', views.topicdetail, name='topic-detail'),
    #ex /upload/topic/add
    path('topic/add',views.addtopic, name='addtopic'),
    path('topic/<int:topicid>/edit', views.editTopic, name='edittopic'),
    path('topicid/<int:topicid>/delete', views.deleteTopic, name='deletetopic'),
    
    # ex: /upload/subject
    path('subject/', views.subject, name='subject'),
    # ex: /upload/subject/add
    path('subject/add', views.addsubject, name='addsubject'),
    # ex: /upload/subject/1
    path('subject/<int:subjectid>', views.editSubject, name='editsubject'),
    path('subject/<int:subjectid>/delete', views.deleteSubject, name='deletesubject'),

    # ex: /upload/question/
    path('question/', views.question, name='question'),    
    #ex /upload/question/art
    path('question/<str:subjectname>',views.questionlist,name='questionlist'),
   
    # eg: /fileupload
    path('fileupload', views.fileupload, name='fileupload'),
     # eg: /fileupload
    path('fileupload/<int:fileid>/delete', views.fileDelete, name='file_delete'),
    # eg: /fileupload/success
    path('fileupload/success', views.fileupload_success, name='fileuploadsuccess'),
    #e.g. /fileupload/process/
    path('fileupload/process/', views.file_processlist, name='fileuploadprocesslist'),
    #e.g. /fileupload/process/1
    
    path('fileupload/process/<int:document_id>', views.fileupload_process, name='fileuploadprocess'),
    path('', views.PersonListView.as_view(), name='person_changelist'),
    path('add/', views.PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-topics/', views.load_topics, name='ajax_load_topics'),
    path('generate-beta/', views.makeQuestion, name='subject_add'),
    # path('generate/', views.makeQuestion, name='subject_add'),



    path('random/', views.questionView.as_view(), name='random'),
    path('createquestions', views.createQuestions, name='createquestions'),
    # path('stats', views.stats,name='stats'),
    # path('stats2', views.stats2,name='stats2'),



 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

 