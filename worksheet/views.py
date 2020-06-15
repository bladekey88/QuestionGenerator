from django.shortcuts import render, redirect
from .forms import SubjectForm
from django.http import HttpResponse, HttpResponseNotAllowed
from docx import Document
import os
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def makeWorkSheet(request):
      if request.method == 'POST':
         raise Exception(request.POST)



      if "subject" not in request.session:
        return redirect('worksheet:selectQuestion')
      else:
         # subject =  request.session['subject']['subjectid']
         subject =  request.session['subject']

      
      
         return render(request,'worksheet/main.html', {'subject':subject})


def selectQuestion(request):
      
      if request.method == 'POST':
         form = SubjectForm(request.POST)
         response_data = {}
         response_data['subjectid'] = request.POST['subjectid']

         request.session['subject'] = response_data
         return redirect('worksheet:worksheet')
         

      else:
         form = SubjectForm()
      
      return redirect('upload:subject_add')
  



def test(request):
   return render(request,'worksheet/test.html')

@csrf_exempt
def word(request):

   if request.method == "POST":
      raise Exception()
   
   document = Document()
   paragraph = document.add_paragraph('Lorem ipsum dolor sit amet.')
   output = "test.docx"
   document.save(output)
   cur = os.getcwd()
   filepath = cur + "/" + output
   with open(filepath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=' + output
            return response
   os.remove(filepaths)
   return HttpResponse(filepath)

