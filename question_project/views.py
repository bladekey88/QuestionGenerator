from upload.models import Question, Topic, Subject, Document
from django.shortcuts import render


def home(request):
    topics = Topic.objects.all().count()
    subjects = Subject.objects.all().count()
    questions = Question.objects.all().count()
    if request.user.is_authenticated:
        files = Document.objects.filter(uploaded_by=request.user).count()
    else:
        files = ""
    context = {
        "topics": topics,
        "subjects": subjects,
        "questions": questions,
        "files": files,
    }
    return render(request, "common/home.html", context)


def bad_request(request, exception):
    context = {}
    return render(request, "common/400.html", context, status=400)


def permission_denied(request, exception):
    context = {}
    return render(request, "common/403.html", context, status=403)


def page_not_found(request, exception):
    context = {}
    return render(request, "common/404.html", context, status=404)


def server_error(request):
    context = {}
    return render(request, "common/500.html", context, status=500)
