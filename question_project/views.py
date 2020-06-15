
from django.http import HttpResponse
from upload.models import Question, Topic, Subject, Document, User, ProcessDocument
from django.shortcuts import render, redirect

def home(request):
    topics = Topic.objects.all().count()
    subjects = Subject.objects.all().count()
    questions = Question.objects.all().count()
    files = Document.objects.all().count()
    context ={
        'topics':topics,
        'subjects':subjects,
        'questions':questions,
        'files': files,
    }
    return render(request, 'common/home.html', context)
    
    
def bad_request(request,exception):
    context = {}
    return render(request, 'common/400.html', context, status=400)


def permission_denied(request,exception):
    context = {}
    return render(request, 'common/403.html', context, status=403)

def page_not_found(request,exception):
    context = {}
    return render(request, 'common/404.html', context, status=404)


def server_error(request):
    context = {}
    return render(request, 'common/500.html', context, status=500)


