from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class UploadFileForm(forms.Form):
    title = forms.CharField()
    file = forms.FileField(label='Select a profile Image')

class QuizForm(forms.Form):
    quizId = forms.IntegerField()
    quizName = forms.CharField(widget=forms.Textarea)
    questionId = forms.IntegerField()
#     currentQuestion =forms.BooleanField(require=False)
    question = forms.CharField()
    correctAnswer = forms.CharField()
    answerOptions = forms.CharField()
    


    


       
