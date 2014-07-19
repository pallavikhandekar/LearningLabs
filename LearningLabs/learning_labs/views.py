from django.shortcuts import render
from django.http.response import HttpResponse
from learning_labs.models import Register, Quiz, QuestionsTable

# Create your views here.

def helloWorld (request):
    return HttpResponse("Welcome Your are on Learning Labs App");

def saveText(request):
    firstname = request.POST.get('fname')
    lastname =  request.POST.get('lname')
    regObj = Register.objects.create( fname=firstname,lname=lastname)
    regObj.save()
    return HttpResponse("Text Saved");

def createQuiz(request):
    quizname =  request.POST.get('quizname');
    question =  request.POST.get('question');
    answerChoices = request.POST.get('answerChoices').split(',');
    correctAnswers =  request.POST.get('correctAnswers').split(',');
    quizObj = Quiz.objects.create(quizname = quizname,question= question, \
                                  answerchoices = answerChoices , correctAnswers = correctAnswers);
    quizObj.save();
    return render(request, "createquiz.html");

def questions(request):
    questions=loadQuestions;
    return render(request, "displayquiz.html", {"questions": questions});

def loadQuestions():
    data = [];
    for obj in Quiz.objects.all().filter(quizname='Quiz 1'):
        question = obj.question;
        answerchoices = ', '.join(obj.answerchoices);
        correctAnswers = ', '.join(obj.correctAnswers);
        data.append({"Questions":question,"Options":answerchoices, "Answer":correctAnswers});
    questions = QuestionsTable(data);
    return questions;