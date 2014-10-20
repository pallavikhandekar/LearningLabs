from django.db import models
from djangotoolbox.fields import ListField
import django_tables2 as tables


#Login / Registration data model
class Register(models.Model):
    fname = models.TextField()
    lname = models.TextField()
    usrname=models.TextField()
    email= models.TextField()
    password = models.TextField()

#Stores Quiz and associated questions and answers choices if any.
class Quiz(models.Model):
    quizname = models.TextField()
    question = models.TextField()
    answerchoices = ListField()
    correctAnswers = ListField()
   
#TODO: Remove / Merge with QUIZ 
class QuestionsTable(tables.Table):
    Questions= tables.Column()
    Options=tables.Column()
    Answer = tables.Column()
    
class pollAnswers(models.Model):
    studentId = models.TextField()
    questionId = models.TextField()
    answer = models.TextField()

class Answers(models.Model):
    Name = models.TextField()
    ID = models.IntegerField()
    SIS_ID = models.IntegerField()
    Section = models.TextField()
    Section_Id = models.IntegerField()
    Section_SIS_Id= models.TextField()
    Question_Id= models.IntegerField()
    Question= models.TextField()
    Submitted= models.TextField()
    Answer= models.TextField()
