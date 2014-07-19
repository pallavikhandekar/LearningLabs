from django.db import models
from djangotoolbox.fields import ListField
import django_tables2 as tables

# Create your models here.
class Register(models.Model):
    fname = models.TextField()
    lname = models.TextField()

class Quiz(models.Model):
    quizname = models.TextField()
    question = models.TextField()
    answerchoices = ListField()
    correctAnswers = ListField()
    
class QuestionsTable(tables.Table):
    Questions= tables.Column()
    Options=tables.Column()
    Answer = tables.Column()
    
class Answers(models.Model):
    quizquestionid = models.TextField()
    userid = models.TextField()
    answer = models.TextField()