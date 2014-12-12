from django.shortcuts import render, redirect,render_to_response
from django.http.response import HttpResponse, HttpResponseRedirect
from learning_labs.models import Register, Quiz, QuestionsTable, PollAnswers,Teams, TopFiveAnswers, ScoreTable,DetailedScoreTable
from django.db.models import  Sum
from django.utils import simplejson
from django.contrib.auth import authenticate, login
from mongoengine.django.auth import User
from django import forms
from django.core.context_processors import csrf, request
from learning_labs.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime


import json
import mining
import os, manage, csv
import geoTracker
from django.core.urlresolvers import reverse

# Stores current question ID
currentQuestionID = 0
quizGlobalId =0

# Create your views here.
questionlist = [];
SITE_ROOT = os.path.dirname(os.path.realpath(manage.__file__));

def helloWorld (request):
    return HttpResponse("Welcome Your are on Learning Labs App");
 
def loadAdminHome (request):
    if request.method == 'GET':
        return render(request, "profile.html", {"form_action":"/home"});
    else:
        studentId = request.POST.get('studentId')
        if not studentId.isdigit():
            return HttpResponse("Incorrect Student ID");
        password = request.POST.get('password')
        regUser = Register.objects.filter(studentId=int(studentId), password=password)
        if len(regUser)!=1: 
            return HttpResponse("Your credentials are wrong");
        else:
            if regUser[0].admin == True:
                obj = regUser[0];
                user = {'name':(obj.fname + " " +obj.lname),'studentId':obj.studentId}
                return render(request, "index.html", {"user":user});
            else:
                return HttpResponse("Access Denied");
     
# Register user : We can remove this
def registerUser(request):
    geodata = geoTracker.getGeoLocationData(request.META['REMOTE_ADDR'])
    if(geodata != None):
        for key, value in geodata.iteritems() :
            print key, value
 
    firstname = request.POST.get('fname')
    lastname = request.POST.get('lname')
    Register.objects.create(fname=firstname, lname=lastname)
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
    readObj = Register.objects.filter(studentId=studentId)
    if not readObj: 
        Register.objects.create(fname=firstname, lname=lastname, usrname=usrname,studentId=int(studentId) ,email=email, password=password)
        return HttpResponse("You are signed up successfully!");
    else:
        return HttpResponse("Your Student ID already exits in record")


def signIn(request):
    studentId = request.POST.get('studentId')
    password = request.POST.get('password')
    readObj = Register.objects.get(studentId=int(studentId), password=password)
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
    quiz_list = set(Quiz.objects.values_list('quizId', flat= True)) #Fetches quiz id from Quiz collection
    if len(quiz_list) ==0:
        return render(request, "selectQuiz.html",{"quiz_list": quiz_list}); #Send empty list to check on html
    else:
        #Fetch the questions:
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
        return render(request, "selectQuiz.html", {"quiz_list": quiz_list, "quizId": int(quizId), "questionToPoll":questionToPoll, "question_list": question_list});         

# Need to work on it for family feud html
def getCurrentQuestion(request):
    questionId = Quiz.objects.get(currentQuestion=True).questionId;
    quizId = Quiz.objects.get(currentQuestion=True).quizId;
    questionName = Quiz.objects.get(questionId=questionId, quizId=quizId).question;
    print questionName
    return render(request, "familyFeudUI.html", {"questionId": questionId, "quizId" : quizId, "questionName":questionName });       
      
           
def setBoolvalue(quizId, questionToPoll):
# Make all the values of CurrentQuestions as False
    questions_list = Quiz.objects.all()
    #print "questions list: "
    for qList in questions_list:
        #print qList.currentQuestion
        qList.currentQuestion = False
        qList.save()          
    # Make CurrentQuestion for selected quizid and question to be true 
    questionId = Quiz.objects.get(quizId=quizId, question=questionToPoll).questionId;
    boolObj = Quiz.objects.get(questionId=questionId, quizId=quizId)
    boolObj.currentQuestion = True
    boolObj.save()



def audienceAnswer(request):
    questionId = None
    quizId = None
    questionName = None
    print request.method;
    if request.method == 'GET':
        try:
            questionId = Quiz.objects.get(currentQuestion=True).questionId;
            quizId = Quiz.objects.get(currentQuestion=True).quizId;
            questionName = Quiz.objects.get(questionId=questionId, quizId=quizId).question;
            print questionId,quizId, questionName
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
        studentExists = Register.objects.filter(studentId=studentId);
        if not studentExists:
            return HttpResponse(simplejson.dumps({"rc":-1, "message":"Incorrect Student Id"}), mimetype='application/json');
        readObj = PollAnswers.objects.filter(studentId=studentId, quizId=quizId, questionId=questionId )
        if not readObj:
            #Check is student exists
            PollAnswers.objects.create(studentId=studentId, questionId=questionId, answer=answer, quizId=quizId, question=questionName)
            return HttpResponse(simplejson.dumps({"rc":0, "message":"Answer saved successfully!"}), mimetype='application/json');
        else:
            return HttpResponse(simplejson.dumps({"rc":-1, "message":"Cannot re-take poll!"}), mimetype='application/json')
    
# Add questions to Quiz
def addQuestion(request):
    quizId = request.POST.get('quizId');
    quizName = request.POST.get('quizName');
    questionId = request.POST.get('questionId');
    question = request.POST.get('question');
    answerOptions = request.POST.get('answerOptions').split(',');
    correctAnswer = request.POST.get('correctAnswer').split(',');
    readObj = Quiz.objects.filter(quizId=quizId, questionId=questionId)
    if not readObj:
        quizObj = Quiz.objects.create(quizId=quizId,quizName=quizName,questionId=questionId,question=question,answerOptions=answerOptions,correctAnswer=correctAnswer);
        quizObj.save();
        #return HttpResponse("Question Saved Successfuly!")
        return redirect('/home/addQuestion');
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

def loadMiningResults(request):
    currentQuiz = Quiz.objects.get(currentQuestion=True);
    if currentQuiz is None:
        return HttpResponse("No Quiz is set");
    else:
        #Quiz is set by Admin using Select quiz/question page
        quiz = Quiz.objects.filter(quizId=currentQuiz.quizId);
        quizDetails={}
        quizDetails['quizId'] = quiz[0].quizId;
        quizDetails['quizName'] = quiz[0].quizName
        questions=[];
        for item in quiz:
            questions.append({'questionId': item.questionId,'question':item.question});
            
        return render(request, 'TextMining/MiningResults.html', {"questions":questions, 'quizDetails': quizDetails }); 

def showChart(request):
    currentQuestion = Quiz.objects.get(currentQuestion=True);
    currentQuestionText = currentQuestion.question;
    currentQuestionId = request.GET.get('quizId') #TODO: Pass current question Id to the getChartData
    currentQuizId = request.GET.get('questionId');#TODO: Pass current quiz Id to the getChartData
    # quizId = request.GET.get('quizId');#TODO: Pass current quiz Id to the getChartData
    # questionId = request.GET.get('questionId');#TODO: Pass current question Id to the getChartData
    chartData = mining.getChartData(currentQuizId,currentQuestionId);
    return HttpResponse(simplejson.dumps({"data":chartData}), mimetype='application/json');

def saveFamilyFeudData(request):
    print "saveFamilyFeudData";
    questionId = request.POST.get('questionId');
    quizId = request.POST.get('quizId');
    data = json.loads(request.POST.getlist("familyFeudData")[0]);
    TopFiveAnswers.objects.filter(quizId=quizId,questionId=questionId).delete(); #Delete if data already exists to over write 
    for obj in data:
        result = TopFiveAnswers();
        result.quizId=quizId;
        result.questionId=questionId; 
        result.answer = obj["answer"];
        result.frequency = obj["frequency"];
        result.save();

    return HttpResponse("Data Saved Successfully");

def fetchFamilyFeudGameData(request):
    print "fetchFamilyFeudGameData";
    response = [];
    #Fetch current Quiz id from current Question.
    quiz = Quiz.objects.get(currentQuestion=True);
    if quiz is None:
        return HttpResponse("Current Quiz not set");
    else:
        #Fetch all questions:
        quizDetails = Quiz.objects.filter(quizId=quiz.quizId);
        gameData=[];
        questions = [];
        #For each question fetch Top5 answers
        for question in quizDetails:
            questions.append({'question':question.question,'questionId':question.questionId});
            topFiveAns = TopFiveAnswers.objects.filter(quizId=quiz.quizId,questionId = question.questionId);
            if len(topFiveAns) == 0:
                return HttpResponse("Data polling pending for question : " + question.question);
            aggregation = TopFiveAnswers.objects.filter(quizId=quiz.quizId,questionId = question.questionId).aggregate(totalSum=Sum('frequency'));
            answerNumber = 0;
            questionData=[];
            for data in topFiveAns:
                answerNumber += 1;
                percentageValue = round((data.frequency*100)/aggregation['totalSum']);
                questionData.append({'answer': data.answer, 'frequency':data.frequency, "answerNumber":++answerNumber,"percentageValue":percentageValue});
        
            gameData.append(questionData)
#       
        return HttpResponse(simplejson.dumps({"questions":questions, "gameData":gameData, "quizId":quiz.quizId }), mimetype='application/json');

def fetchFamilyFeudGameScores(request):
    quizId =  Quiz.objects.get(currentQuestion=True).quizId;
    score = ScoreTable.objects.filter(QuizId=quizId);
    gameScores = {};
    if len(score)==1:
        obj = score[0];
        gameScores['Team1Score'] = obj.Team1Score;
        gameScores['Team2Score'] = obj.Team2Score;
    else:
        gameScores['Team1Score'] = 0;
        gameScores['Team2Score'] = 0;
    return HttpResponse(simplejson.dumps({"gameScores":gameScores}), mimetype='application/json');

# ***************END TEXT MINING SECTION ******************
# *************** Import Student Data ************
def uploadStudentData(request):
    if request.method == 'POST':
        file = request.FILES['file'];
        try:
            saveStudentDataToMongo(file);
            return redirect('/home/UploadStudent');
        except Exception as e:
            Errormessage = "FILE should be , separated csv with data in format"
            return HttpResponse(Errormessage);
    return HttpResponse("Data saved unsuccessfully!");

# ****************Import Quiz Data****************
def uploadQuizData(request):
    if request.method == 'POST':
        file = request.FILES['file'];
        try:
            saveCSVToMongo(file);
            return redirect('/home/UploadQuiz');
        except Exception as e:
            Errormessage = "FILE should be , separated csv with data in format Quiz Id, Quiz Name, Question Id, Question, Correct Ans (if any else ""), Answer Options for Quiz (if any else "")"
            return HttpResponse(Errormessage);
    return HttpResponse("Data saved unsuccessfully!");

def saveStudentDataToMongo(file):
    dataReader = csv.reader(file)
    # print(file.get_full_path())
    for row in dataReader:
        print(row[0])
        studentObj = Register();
        studentObj.fname = row[0];
        studentObj.lname = row[1];
        studentObj.usrname = row[2];
        studentObj.studentId = row[3];
        studentObj.email = row[4];
        studentObj.password = row[5];
        studentObj.teamNameProject = row[6];
        studentObj.save();
    # firstname = request.POST.get('fname')
    # lastname = request.POST.get('lname')
    # email = request.POST.get('email')
    # usrname = request.POST.get('usrname')
    # studentId = request.POST.get('studentId')
    # password = request.POST.get('password')
    # readObj = Register.objects.filter(studentId=studentId)
    # if not readObj:
    #     Register.objects.create(fname=firstname, lname=lastname, usrname=usrname,studentId=int(studentId) ,email=email, password=password)
    #     return HttpResponse("You are signed up successfully!");
    # else:
    #     return HttpResponse("Your Student ID already exits in record")
 
def saveCSVToMongo(file):
#     csvFilePath = SITE_ROOT + '/static/QuestionsList.csv';
    quizId  = -1;
    dataReader = csv.reader(file)
    for row in dataReader:
        quizObj = Quiz();
        if quizId != int(row[0]):
            quizId = int(row[0]);
            Quiz.objects.filter(quizId=quizId).delete(); #Delete Quiz before uploading.
            
        quizObj.quizId = row[0];
        quizObj.quizName = row[1];
        quizObj.questionId = row[2];
        if row[3].lower() == "true":
            quizObj.currentQuestion = True;
        else:
            quizObj.currentQuestion = False;
        quizObj.question = row[4];
        quizObj.correctAnswer = row[5];
        quizObj.answerOptions = row[6];
        quizObj.save();
        
#****************End Import Quiz Data****************

#****************Create Teams******************
# Create Team method, populates Entire student data to admin where admin can select students and put them in team
def createTeams(request):
    if request.method == 'GET':
        try:
            queryset = Register.objects.all().order_by('teamNameProject')
            print([p.lname for p in queryset])
            return render(request, "createTeams.html", {"queryset":queryset });       
        except Exception as e:
            Errormessage = "Some thing is wrong with student record"
            return HttpResponse('Sorry! No data found')
         
    else:
        teamName= request.POST.get('teamName')
        gameDate = request.POST.get('datetime')
        date, time = gameDate.split(" ")
        chngFormat = datetime.strptime(gameDate,"%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
        print "Changed format" + chngFormat
        studentDetail = request.POST.getlist('selStudent')
        for q in studentDetail:
            teamNameProject,studentId,fname,lname = q.split(",")
            Teams.objects.create(teamName=teamName, gameDate=chngFormat,studentId=int(studentId),lname=lname,fname=fname,teamNameProject=teamNameProject )
        return redirect('/home/createTeams');

# Score Section************
def saveScore(request):
    DetailScores =  json.loads(request.POST.get('DetailScores'));
    gameScore =  json.loads(request.POST.get('gameScore'));

    #Fetch scoretable score. 
    scores = ScoreTable.objects.filter(QuizId=gameScore['QuizId']);
    score = scores[0];
    score.Team1Score = gameScore['Team1Score'];
    score.Team2Score = gameScore['Team2Score'];
    score.save();
    
    detailedScores = DetailedScoreTable.objects.filter(QuizId=gameScore['QuizId']);

    for counter in range(0, len(detailedScores)):
        obj = detailedScores[counter];
        obj.Team1Score = DetailScores[counter]['Team1Score'];
        obj.Team2Score = DetailScores[counter]['Team2Score'];    
        obj.save();
        
    return HttpResponse("Data saved unsuccessfully!");
   

def displayScorePage(request):
    currentQuiz = Quiz.objects.get(currentQuestion=True);
    quizId = currentQuiz.quizId;
    quizName = currentQuiz.quizName;
    questions = Quiz.objects.filter(quizId=quizId);
    questionCount = Quiz.objects.filter(quizId=quizId).count();
    gameData=[];
    questionNumber = 1;
    createObjects = False;
    
    #Fetch detailed score
    detailedscores = DetailedScoreTable.objects.filter(QuizId=quizId);
    if len(detailedscores) == 0: #No scores created
        createObjects = True;
        detailedscores = [];
   
            
    for question in questions:
        if createObjects: #for fist time
            obj = DetailedScoreTable.objects.create(QuizId=quizId,QuestionId=question.questionId, QuestionName=question.question,Team1Score=0,Team2Score=0);
            detailedscores.append(obj);
            
        topFiveAns = TopFiveAnswers.objects.filter(quizId=quizId,questionId = question.questionId);
        if len(topFiveAns) == 0:
            return HttpResponse("Data polling pending for question : " + question.question);
        aggregation = TopFiveAnswers.objects.filter(quizId=quizId,questionId = question.questionId).aggregate(totalSum=Sum('frequency'));
        answerNumber = 0;
        obj = None;
        answers = []
        for data in topFiveAns:
            answerNumber += 1;
            percentageValue = round((data.frequency*100)/aggregation['totalSum']);
            obj = GameData(questionNumber,question.question,data.answer,data.frequency,++answerNumber,percentageValue);
            answers.append(obj);

        gameData.append(answers)
        questionNumber +=1;
        

    gamescore = ScoreTable.objects.filter(QuizId=quizId);
    if len(gamescore) == 0: #No scores created
        gamescore = ScoreTable.objects.create(QuizId=quizId,QuizName=quizName,Team1Score=0,Team2Score=0);
    else:
        gamescore = gamescore[0];
        
    return render(request, "score.html", {"quizId" : quizId,"questionCount" : questionCount,"questions" : questions,"gameData":gameData, "detailedscores":detailedscores,"gamescore":gamescore});


class GameData:
    def __init__(self, questionNumber,question, answer, frequency,answerNumber,percentageValue):
        self.questionNumber = questionNumber
        self.question = question
        self.answer = answer
        self.frequency = frequency
        self.answerNumber = answerNumber
        self.percentageValue = percentageValue
# Score Section************