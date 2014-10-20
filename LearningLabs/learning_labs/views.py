from django.shortcuts import render
from django.http.response import HttpResponse
# from django.template import Context, loader
from learning_labs.models import Register, Quiz, QuestionsTable,pollAnswers
from django.utils import simplejson
from django.contrib.auth import authenticate, login
import geoTracker
from django import forms
import mining



# Create your views here.
questionlist=[];
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
    
    regObj = Register.objects.create(fname=firstname,lname=lastname, usrname=usrname, email=email, password=password)
    regObj.save()
    return HttpResponse("Sign up");

def audienceAnswer(request):
    studentId = request.POST.get('studentId')
    questionId = request.POST.get('questionId')
    answer = request.POST.get('answer')
    
    aaObj = pollAnswers.objects.create(studentId=studentId,questionId=questionId, answer=answer)
    aaObj.save()
    return HttpResponse("Answer Saved Successfuly!");

# def signIn(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             return HttpResponse("Signed in")
#         else:
#             return HttpResponse("Not Signed in")
#     else:
#         return HttpResponse("Not Signed in")

def signIn(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return HttpResponse({'state':state, 'username': username})
 
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
