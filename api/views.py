import django_filters.rest_framework
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import QuestionSerialiser,TopicSerialiser,SubjectSerialiser,QuestionBasicSerialiser, UserSerialiser,GroupSerialiser, LoginSerialiser
from rest_framework import viewsets
from upload.models import Question,Topic,Subject,User
from rest_framework import permissions
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from .filters import QuestionFilterSet
from django.http import HttpResponse
from rest_framework.response import Response

from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.authentication import BasicAuthentication
from knox.models import AuthToken    
from django.contrib import messages

# Create your views here.

@login_required
def generateAPIKey(request):

    user_groups = list(request.user.groups.all().values_list("name",flat=True))
    if any("teacher" in s for s in user_groups):
        tokens = AuthToken.objects.filter(user_id=request.user).values_list("token_name","created","expiry","digest").order_by("-expiry")        
        token_data = [(token[0],token[1],token[2],token[3]) for token in tokens]

        # from django.contrib.auth.models import Permission
        # p = Permission.objects.all().values_list()



    else:
        token_data=None
        messages.error(request,"<h4 class='text-center font-weight-bolder'>Access Denied</h4><h5 class='text-center'>Only teachers may use API functions.</h5>")

    return render(request, "api/generate-key.html", {"token_data":token_data})




class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('subjectid__subjectname','topicid__topicname')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_class = QuestionFilterSet
    def get_serializer_class(self):
        user_groups = list(self.request.user.groups.all().values_list("name",flat=True))
        if any("teacher" in s for s in user_groups):
            return QuestionSerialiser
        else:
            return QuestionBasicSerialiser

 
    


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('-topicname')
    serializer_class = TopicSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('-subjectname')
    serializer_class = SubjectSerialiser
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerialiser
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerialiser
    permission_classes = [permissions.DjangoModelPermissions]    


class SubjectQuestiontViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    model = Question
    serializer_class = QuestionSerialiser
    queryset = Question.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_fields = ['subjectid__subjectname']

class PurchaseList(generics.ListAPIView):
    serializer_class = QuestionSerialiser

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        subject = self.kwargs['subject']
        return Question.objects.filter(subjectid__subjectname=subject)



class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request, format=None):
        serializer = LoginSerialiser(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        return super(LoginView, self).post(request, format=None)        



     