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
    email = models.TextField()
    password = models.TextField()

# Stores Quiz and associated questions and answers choices if any.
class Quiz(models.Model):
    quizId = models.IntegerField()
    quizName = models.TextField()
    questionID = models.IntegerField()
    question = models.TextField()
    correctAnswer = models.TextField()
    answerOptions = models.TextField()
    
class pollAnswers(models.Model): 
    questionId = models.TextField()
    quizId = models.IntegerField()
    studentId = models.TextField()
    quizName = models.TextField()
    answer = models.TextField()
    
# TODO: Remove / Merge with QUIZ 
class QuestionsTable(tables.Table):
    Question = tables.Column()
    Options = tables.Column()
    Answer = tables.Column()
    
# # TODO: Remove 
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
    

# class Document(models.Model):
#     title = models.CharField(max_length=200)
#     thumbnail = models.FileField()
    
# def get_upload_file_name(instance, filename):
#     return "uploaded_files/ %s_%s" % (str(time)()).replace('.', '_'), filename
    
