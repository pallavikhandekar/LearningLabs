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
    url(r'Register', TemplateView.as_view(template_name='./index.html')), 
    url(r'savedText$', views.saveText),   
    url(r'AddQuestion', TemplateView.as_view(template_name='./createquestions.html')), 
    url(r'addQuestion', views.addQuestion),     
    url(r'DisplayQuiz', views.displayquestions),
    url(r'CreateQuiz', TemplateView.as_view(template_name='./quiz.html'))
    
)
