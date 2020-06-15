from django import forms
from upload.models import Subject, Question


class SubjectForm(forms.ModelForm):
     
    
   
    class Meta:    
        model = Question  
        fields = ['subjectid',]
        
        
    field_order = ['subjectid',]
    #Override params by cleaning it up :)
    