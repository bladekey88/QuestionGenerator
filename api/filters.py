import django_filters
from upload.models import Question
from django_filters import rest_framework as filters

class QuestionFilterSet(filters.FilterSet):
    subject = django_filters.CharFilter(field_name='subjectid__subjectname')
    
    class Meta:
        model = Question
        fields = ['subjectid',]


