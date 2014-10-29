from django.db import models
from djangotoolbox.fields import ListField
import django_tables2 as tables
from django import forms
from time import time
from django.contrib.auth.models import User

# Login / Registration data model
class Register(models.Model):
    fname = models.TextField()
    lname = models.TextField()
    usrname = models.TextField()
    studentId = models.IntegerField().primary_key()
    email = models.EmailField()
    password = models.TextField()

# Stores Quiz and associated questions and answers choices if any.
class Quiz(models.Model):
    quizId = models.IntegerField()
    quizName = models.TextField()
    questionId = models.IntegerField()
    currentQuestion =models.BooleanField(default=False)
    question = models.TextField()
    correctAnswer = models.TextField()
    answerOptions = models.TextField()
    
class PollAnswers(models.Model): 
    questionId = models.IntegerField()
    quizId = models.IntegerField()
    question = models.TextField()
    studentId = models.TextField()
    answer = models.TextField()




#*********************************************************************#
# we can remove this model
class QuestionsTable(tables.Table):
    Question = tables.Column()
    Options = tables.Column()
    Answer = tables.Column()
    
# we can remove this model
class Answers(models.Model):
    Name = models.TextField()
    ID = models.IntegerField()
    SIS_ID = models.IntegerField()
    Section = models.TextField()
    Section_Id = models.IntegerField()
    Section_SIS_Id = models.TextField()
    Question_Id = models.IntegerField()
    Question = models.TextField()
    Submitted = models.TextField()
    Answer = models.TextField() 
#*********************************************************************#
    
