from django.conf.urls import patterns, include, url
from django.contrib import admin
from learning_labs import views;
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LearningLabs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    

    url(r'^admin/', include(admin.site.urls)),
    url(r'registerUser$', views.registerUser),
    url(r'countpolls', views.getPolls),
    url(r'counter', TemplateView.as_view(template_name='./counter.html')),
    url(r'polls', TemplateView.as_view(template_name='./Polls.html')),
    url(r'answerQuestions', views.answerQuestions),
    url(r'AddQuestion', TemplateView.as_view(template_name='./createquestions.html')), 
    url(r'addQuestion', views.addQuestion),     
    url(r'DisplayQuiz', views.displayquestions),
    url(r'CreateQuiz', TemplateView.as_view(template_name='./base.html')),
    url(r'AdminProfile', TemplateView.as_view(template_name='./AdminProfile.html')),
    url(r'answerquiz/(?P<quizname>\w+)/(?P<question>[\w|\W]+)', views.answer),
    url(r'FamilyFeudGame',TemplateView.as_view(template_name='./familyFeudUI.html')),
    
    url(r'Profile',TemplateView.as_view(template_name='./profile.html')),
    url(r'signUp$', views.signUp),
    url(r'signIn$', views.signIn),
    
    url(r'Audiencepoll',views.audienceAnswer),
    url(r'answerSaved', views.audienceAnswer),

    url(r'answer',TemplateView.as_view(template_name='./answer.html')),
    
    url(r'Upload',TemplateView.as_view(template_name='./upload.html')),
    url(r'^uploadFile/$', views.uploadFile),
    
    #**********Text Mining Section ***********
    url(r'miningresults',views.showChart),
    
    # ******End Text Mining Section **********
    url(r'Dashboard',TemplateView.as_view(template_name='./dashboard.html'))
    

)
