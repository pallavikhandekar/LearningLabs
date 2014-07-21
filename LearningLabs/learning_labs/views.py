from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import Context, loader
from learning_labs.models import Register, Quiz, QuestionsTable, Answers
import datetime

# Create your views here.
questionlist=[];
def helloWorld (request):
    return HttpResponse("Welcome Your are on Learning Labs App");

#Register user
def saveText(request):
    firstname = request.POST.get('fname')
    lastname =  request.POST.get('lname')
    regObj = Register.objects.create( fname=firstname,lname=lastname)
    regObj.save()
    return HttpResponse("Text Saved");

#Add questions to Quiz
def addQuestion(request):
    quizname =  request.POST.get('quizname');
    question =  request.POST.get('question');
    answerChoices = request.POST.get('answerChoices').split(',');
    correctAnswers =  request.POST.get('correctAnswers').split(',');
    quizObj = Quiz.objects.create(quizname = quizname,question= question, \
                                  answerchoices = answerChoices , correctAnswers = correctAnswers);
    quizObj.save();
    loadQuestions(quizname);
    return render(request, "createquestions.html");

#Display questions for a Quiz
def displayquestions(request):
    data = QuestionsTable(questionlist);
    if not questionlist:
        temp = [];
        temp.append({"Questions":'',"Options":'', "Answer":''});
        data=QuestionsTable(temp)
    return render(request, "displayquiz.html", {"questions": data});

#Save answer for a question for a user
def answerQuestions(request):
    quizquestionid =  request.POST.get('quiz');
    userid =  request.POST.get('userId');
    answer = request.POST.get('answer');
    answerObj = Answers.objects.create(quizquestionid=quizquestionid,userid=userid,answer=answer);
    answerObj.save();
    return HttpResponse("Answer saved successfully!");

#Load Questions for a Quiz
def questions(request):
    quizname =  request.POST.get('quizname');
    loadQuestions(quizname);
    return render(request, "");

def loadQuestions(quizname):
    for obj in Quiz.objects.all().filter(quizname=quizname):
        question = obj.question;
        answerchoices = ', '.join(obj.answerchoices);
        correctAnswers = ', '.join(obj.correctAnswers);
        questionlist.append({"Questions":question,"Options":answerchoices, "Answer":correctAnswers});

def answer(request,quizname,question):
    thequestion=""
    try:
        thequestion =Quiz.objects.get(quizname=quizname,question=question)
    except:
        thequestion = "";
    return render(request,'answer.html',{"thequestion":thequestion})

def saveAnswer(request):
    quizId =  request.POST.get('quiz');
    answer = request.POST.get('answer')
    userId = request.POST.get('userId')

