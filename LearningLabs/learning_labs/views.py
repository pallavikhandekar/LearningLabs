from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from learning_labs.models import Register, Quiz, QuestionsTable,pollAnswers
from django.utils import simplejson
from django.contrib.auth import authenticate, login
from mongoengine.django.auth import User
from django import forms
from django.core.context_processors import csrf, request
from learning_labs.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext

import mining
import os, manage, csv
import geoTracker

#Stores current question ID
currentQuestionID = 0

# Create your views here.
questionlist=[];
SITE_ROOT = os.path.dirname(os.path.realpath(manage.__file__));

def helloWorld (request):
    return HttpResponse("Welcome Your are on Learning Labs App");

#Register user
def registerUser(request):
    geodata = geoTracker.getGeoLocationData(request.META['REMOTE_ADDR'])
    if(geodata!=None):
        for key, value in geodata.iteritems() :
            print key, value

    firstname = request.POST.get('fname')
    lastname =  request.POST.get('lname')
    regObj = Register.objects.create( fname=firstname,lname=lastname)
    regObj.save()
    if(geodata!=None):
        return HttpResponse(str(geodata));
    else:
        return HttpResponse('Text Saved');
    
def signUp(request):
    firstname = request.POST.get('fname')
    lastname =  request.POST.get('lname')
    email = request.POST.get('email')
    usrname = request.POST.get('usrname')
    password = request.POST.get('password')
    
    regObj = User.objects.create(first_name=firstname,last_name=lastname, username=usrname, email=email, password=password)
    regObj.save()
    return HttpResponse("You are signed up successfully!");


def signIn(request):
    username = request.POST.get('usrname','')
    password = request.POST.get('password','')
    obj = User.objects.get(username=username, password=password)
    
    if obj is not None:
        if obj.is_active:
            return HttpResponse("Signed in")
        else:
            return HttpResponse("Not Signed in")
    else:
        return HttpResponse("Not Signed in")

    
def populateQuiz(request):
    entry_list = set(Quiz.objects.values_list('quizId', flat=True))
    quizId = request.POST.get('quizIdToPoll')
    question_list = Quiz.objects.values_list('question', flat=True).filter(quizId = quizId)
    questionToPoll = request.POST.get('questionToPoll')
    print quizId
    if questionToPoll is not None:
        print questionToPoll
        setBoolvalue(quizId,questionToPoll);
    print "inPopulateQuiz"
    return render(request, "selectQuiz.html", {"entry_list": entry_list, "question_list":question_list});

def setBoolvalue(quizId,questionToPoll):
    print "insetbool"
    print "insetbool"+ quizId
    print "insetbool"+ questionToPoll
    questionId = Quiz.objects.get(quizId = quizId,question= questionToPoll).questionId;
    boolObj = Quiz.objects.get(questionId=questionId, quizId=quizId)
    booli= boolObj.currentQuestion;
    booli = True
    boolObj.currentQuestion = booli
    boolObj.save()
    
#     obj.currentQuestion = True

def audienceAnswer(request):
    # Assumption: we have quiz and current question
#     questionId = 7;
#     quizId = 1;
    questionId= Quiz.objects.get(currentQuestion=True).questionId;
    quizId = Quiz.objects.get(currentQuestion=True).quizId;
    print questionId,quizId
    questionName = Quiz.objects.get(questionId=questionId, quizId=quizId).question;
    if request.method == 'GET':
        boolObj = Quiz.objects.get(questionId=questionId, quizId=quizId)
        booli= boolObj.currentQuestion;
        booli = False
        boolObj.currentQuestion = booli
        boolObj.save()
        print questionName
        return render(request, "audiencepoll.html", {"questionId": questionId, "quizId" : quizId, "questionName":questionName });
    else:
        studentId = request.POST.get('studentId')
        quizId = request.POST.get('quizId')
        questionId = request.POST.get('questionId')
        answer = request.POST.get('answer')
#         questionName = request.POST.get('questionName')
#         print questionName
        aaObj = pollAnswers.objects.create(studentId=studentId, questionId=questionId, answer=answer, quizId=quizId, question=questionName)
        aaObj.save()
        return HttpResponse("Answer Saved Successfuly!")
    
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
    answerObj = answer.objects.create(quizquestionid=quizquestionid,userid=userid,answer=answer);
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

def getPolls(request):
    queryset = answer.objects.all();
    response_data = {};
    count =queryset.count();
    response_data['count'] = count;
    print count;
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json');

#*****************TEXT MINING SECTION ******************

def showChart(request):
    chartData = mining.getChartData();
    return render(request, 'TextMining/MiningResults.html', {"data":chartData})

# ***************END TEXT MINING SECTION ******************

# ****************Import Quiz Data****************
def uploadFile(request):
    if request.method == 'POST':
        file = request.FILES['file'];
        try:
            saveCSVToMongo(file);
            return render(request, 'upload.html');
        except Exception as e:
            Errormessage = "FILE should be , separated csv with data in format Quiz Id, Quiz Name, Question Id, Question, Correct Ans (if any else "")," 
            +"Answer Options for Quiz (if any else "")"
            return HttpResponse('/success/url/')
    else:
        form = UploadFileForm()
    return HttpResponse("Data saved unsuccessfully!");
 
def saveCSVToMongo(file):
#     csvFilePath = SITE_ROOT + '/static/QuestionsList.csv';
    dataReader = csv.reader(file, delimiter=',', quotechar='"')
    for row in dataReader:
        quizObj = Quiz();
        quizObj.quizId= row[0];
        quizObj.quizName = row[1];
        quizObj.questionId = row[2];
        quizObj.currentQuestion = row[3];
        quizObj.question = row[4];
        quizObj.correctAnswer = row[5];
        quizObj.answerOptions = row[6];
        quizObj.save();
#****************End Import Quiz Data****************
