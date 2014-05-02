from django.shortcuts import render
from django.http.response import HttpResponse
from learning_labs.models import Register

# Create your views here.

def helloWorld (request):
    return HttpResponse("Welcome Your are on Learning Labs App");

def saveText(request):
    firstname = request.POST.get('fname')
    lastname =  request.POST.get('lname')
    regObj = Register.objects.create( fname=firstname,lname=lastname)
    regObj.save()
    return HttpResponse("Text Saved");