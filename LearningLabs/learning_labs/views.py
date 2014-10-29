from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from learning_labs.models import Register, Quiz, QuestionsTable, pollAnswers
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

# Stores current question ID
currentQuestionID = 0
quizGlobalId =0

# Create your views here.
questionlist = [];
SITE_ROOT = os.path.dirname(os.path.realpath(manage.__file__));

def helloWorld (request):
    return HttpResponse("Welcome Your are on Learning Labs App");

# Register user
def registerUser(request):
    geodata = geoTracker.getGeoLocationData(request.META['REMOTE_ADDR'])
    if(geodata != None):
        for key, value in geodata.iteritems() :
            print key, value

    firstname = request.POST.get('fname')
    lastname = request.POST.get('lname')
    regObj = Register.objects.create(fname=firstname, lname=lastname)
    regObj.save()
    if(geodata != None):
        return HttpResponse(str(geodata));
    else:
        return HttpResponse('Text Saved');
    
def signUp(request):
    firstname = request.POST.get('fname')
    lastname = request.POST.get('lname')
    email = request.POST.get('email')
    usrname = request.POST.get('usrname')
    studentId = request.POST.get('studentId')
    password = request.POST.get('password')
    readObj = pollAnswers.objects.filter(studentId=studentId)
    if not readObj: 
        regObj = Register.objects.create(fname=firstname, lname=lastname, usrname=usrname,studentId=studentId ,email=email, password=password)
        regObj.save()
        return HttpResponse("You are signed up successfully!");
    else:
        return HttpResponse("Your Student ID already exits in record")


def signIn(request):
    studentId = request.POST.get('studentId')
    password = request.POST.get('password')
    readObj = Register.objects.filter(studentId=studentId, password=password)
    if not readObj: 
        return HttpResponse("Your credentials are wrong");
    else:
        return HttpResponse("You are signdin successfully");
    
def resetPassword(request):
    studentId = request.POST.get('studentId')
    newPassword = request.POST.get('newPassword')
    confirmPassword = request.POST.get('confirmPassword')
    
    readObj = Register.objects.filter(studentId=studentId)
    print readObj;
    if not readObj:
        return HttpResponse("Student ID doesnt exist");
    else:
        if newPassword == confirmPassword:
            Register.objects.filter(studentId=studentId).update(password=confirmPassword)
            return HttpResponse("Your password updated successfully");
        else:
            return HttpResponse("Your passwords dont match");
    
    
def populateQuiz(request):
    entry_list = set(Quiz.objects.values_list('quizId', flat= True))
    quizId = request.POST.get('quizIdToPoll')
    question_list = Quiz.objects.values_list('question', flat=True).filter(quizId=quizId)
    questionToPoll = request.POST.get('questionToPoll')
    
    if quizId is None:
        quizId = 1
        print  "quiz id is: 1"
        
    if questionToPoll is not None:
        print "question poll is:"
        print questionToPoll
        setBoolvalue(quizId, questionToPoll);
   
    return render(request, "selectQuiz.html", {"entry_list": entry_list, "quizId": int(quizId), "questionToPoll":questionToPoll, "question_list": question_list});
        

def setBoolvalue(quizId, questionToPoll):
# Make all the values of CurrentQuestions as False
    questions_list = Quiz.objects.all()
    print "questions list: "
    for qList in questions_list:
        print qList.currentQuestion
        qList.currentQuestion = False
        qList.save()          
# Make CurrentQuestion for selected quizid and question to be true 
    questionId = Quiz.objects.get(quizId=quizId, question=questionToPoll).questionId;
    boolObj = Quiz.objects.get(questionId=questionId, quizId=quizId)
    booli = boolObj.currentQuestion;
    booli = True
    boolObj.currentQuestion = booli
    boolObj.save()

def audienceAnswer(request):
    questionId = None
    quizId = None
    questionName = None
    if request.method == 'GET':
        try:
            questionId = Quiz.objects.get(currentQuestion=True).questionId;
            quizId = Quiz.objects.get(currentQuestion=True).quizId;
            questionName = Quiz.objects.get(questionId=questionId, quizId=quizId).question;
            print questionName
            return render(request, "audiencepoll.html", {"questionId": questionId, "quizId" : quizId, "questionName":questionName });       
        except Exception as e:
            Errormessage = "Poll is closed question is not selected yet"
            return HttpResponse('Poll is closed question is not selected yet')
        
    else:
        studentId = request.POST.get('studentId')
        quizId = request.POST.get('quizId')
        questionId = request.POST.get('questionId')
        answer = request.POST.get('answer')
        questionName = request.POST.get('questionName')
        print studentId, quizId, quizId, questionName 
        readObj = pollAnswers.objects.filter(studentId=studentId, quizId=quizId, questionId=questionId )
        print readObj;
        if not readObj:
            aaObj = pollAnswers.objects.create(studentId=studentId, questionId=questionId, answer=answer, quizId=quizId, question=questionName)
            aaObj.save()
            return HttpResponse("Answer Saved Successfuly!")
        else:
            return HttpResponse("Cannot retake poll!")
    
# Add questions to Quiz
def addQuestion(request):
    quizId = request.POST.get('quizId');
    quizName = request.POST.get('quizName');
    questionId = request.POST.get('questionId');
    question = request.POST.get('question');
#     answerOptions = request.POST.get('answerOptions');
#     correctAnswer = request.POST.get('correctAnswer');
    answerOptions = request.POST.get('answerOptions').split(',');
    correctAnswer = request.POST.get('correctAnswer').split(',');
    readObj = Quiz.objects.filter(quizId=quizId, questionId=questionId)
    if not readObj:
        quizObj = Quiz.objects.create(quizId=quizId,quizName=quizName,questionId=questionId,question=question,answerOptions=answerOptions,correctAnswer=correctAnswer);
        quizObj.save();
#       loadQuestions(quizName);
#       return render(request, "createquestions.html");
        return HttpResponse("Question Saved Successfuly!")
    else:
        return HttpResponse("This question Id for quiz ID already exits! Make it unique")

# Display questions for a Quiz
def displayquestions(request):
    data = QuestionsTable(questionlist);
    if not questionlist:
        temp = [];
        temp.append({"Questions":'', "Options":'', "Answer":''});
        data = QuestionsTable(temp)
    return render(request, "displayquiz.html", {"questions": data});

# Save answer for a question for a user
def answerQuestions(request):
    quizquestionid = request.POST.get('quiz');
    userid = request.POST.get('userId');
    answer = request.POST.get('answer');
    answerObj = answer.objects.create(quizquestionid=quizquestionid, userid=userid, answer=answer);
    answerObj.save();
    return HttpResponse("Answer saved successfully!");

# Load Questions for a Quiz
def questions(request):
    quizname = request.POST.get('quizname');
    loadQuestions(quizname);
    return render(request, "");

def loadQuestions(quizname):
    for obj in Quiz.objects.all().filter(quizname=quizname):
        question = obj.question;
        answerchoices = ', '.join(obj.answerchoices);
        correctAnswers = ', '.join(obj.correctAnswers);
        questionlist.append({"Questions":question, "Options":answerchoices, "Answer":correctAnswers});

def answer(request, quizname, question):
    thequestion = ""
    try:
        thequestion = Quiz.objects.get(quizname=quizname, question=question)
    except:
        thequestion = "";
    return render(request, 'answer.html', {"thequestion":thequestion})

def getPolls(request):
    queryset = answer.objects.all();
    response_data = {};
    count = queryset.count();
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
            return redirect('/home/Upload');
        except Exception as e:
            Errormessage = "FILE should be , separated csv with data in format Quiz Id, Quiz Name, Question Id, Question, Correct Ans (if any else ""), Answer Options for Quiz (if any else "")"
            return HttpResponse(Errormessage)
    else:
        form = UploadFileForm()
    return HttpResponse("Data saved unsuccessfully!");
 
def saveCSVToMongo(file):
#     csvFilePath = SITE_ROOT + '/static/QuestionsList.csv';
    dataReader = csv.reader(file, delimiter=',', quotechar='"')
    for row in dataReader:
        quizObj = Quiz();
        quizObj.quizId = row[0];
        quizObj.quizName = row[1];
        quizObj.questionId = row[2];
        quizObj.currentQuestion = row[3];
        quizObj.question = row[4];
        quizObj.correctAnswer = row[5];
        quizObj.answerOptions = row[6];
        quizObj.save();
#****************End Import Quiz Data****************
