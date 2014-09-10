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
    #url(r'^', views.helloWorld),
    url(r'Register', TemplateView.as_view(template_name='./register.html')), 
    url(r'registerUser$', views.registerUser),
    url(r'countpolls', views.getPolls),
    url(r'counter', TemplateView.as_view(template_name='./counter.html')),
    url(r'polls', TemplateView.as_view(template_name='./Polls.html')),
    url(r'answerQuestions', views.answerQuestions),
    url(r'AddQuestion', TemplateView.as_view(template_name='./createquestions.html')), 
    url(r'addQuestion', views.addQuestion),     
    url(r'DisplayQuiz', views.displayquestions),
    url(r'CreateQuiz', TemplateView.as_view(template_name='./quiz.html')),
    url(r'answerquiz/(?P<quizname>\w+)/(?P<question>[\w|\W]+)', views.answer),
    url(r'FamilyFeudGame',TemplateView.as_view(template_name='./familyFeudUI.html'))  
)
