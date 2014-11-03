from django.conf.urls import patterns, include, url
from django.contrib import admin
from learning_labs import views;
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'registerUser$', views.registerUser),
    url(r'countpolls', views.getPolls),
    url(r'counter', TemplateView.as_view(template_name='./counter.html')),
    url(r'polls', TemplateView.as_view(template_name='./Polls.html')),
    url(r'answerQuestions', views.answerQuestions),     
    url(r'DisplayQuiz', views.displayquestions),
    url(r'CreateQuiz', TemplateView.as_view(template_name='./base.html')),
    url(r'AdminProfile', TemplateView.as_view(template_name='./AdminProfile.html')),
    url(r'popQuiz$', views.populateQuiz),
    
    url(r'answerquiz/(?P<quizname>\w+)/(?P<question>[\w|\W]+)', views.answer),
    url(r'FamilyFeudGame',TemplateView.as_view(template_name='./familyFeudUI.html')),
#     url(r'FamilyFeudGame',views.getCurrentQuestion),
#      
    url(r'Profile',TemplateView.as_view(template_name='./profile.html')),
    url(r'signUp$', views.signUp),
    url(r'signIn$', views.signIn),
    url(r'ResetPassword', TemplateView.as_view(template_name='./resetPassword.html')),
    url(r'resetPassword', views.resetPassword),
    
    url(r'Audiencepoll',views.audienceAnswer),
    url(r'answerSaved', views.audienceAnswer),
    
    url(r'createTeams',views.createTeams),
    url(r'answerSaved', views.createTeams),

    url(r'answer',TemplateView.as_view(template_name='./answer.html')),
    url(r'myTest',TemplateView.as_view(template_name='./tempTest.html')),
    
    #url(r'Upload$',TemplateView.as_view(template_name='./upload.html')),
    url(r'^uploadFile/$', views.uploadFile),
    url(r'^importCsv/$', views.saveCSVToMongo),
    
    #**********Text Mining Section ***********
    url(r'miningResults',views.showChart),
    
    # ******End Text Mining Section **********

    #******* URL for Template ***************
    url(r'^home$',TemplateView.as_view(template_name='./index.html')),
    url(r'^home/Upload/$',TemplateView.as_view(template_name='./upload.html')),
  
# #     url(r'CreateTeams',TemplateView.as_view(template_name='./createTeams.html')),
#     url(r'^createTeams/',views.createTeams,name='createTeams'),

    url(r'^home/selectQuiz$',views.populateQuiz),
    
    url(r'^home/addQuestion$', TemplateView.as_view(template_name='./createquestions.html')),
    url(r'addQuestion', views.addQuestion),
    
    url(r'^home/createTeams$',views.createTeams),
    url(r'^home/miningResults$',views.showChart)
    #******* END URL for Template ***************
    #******* URL for Template ***************

   
    
)
