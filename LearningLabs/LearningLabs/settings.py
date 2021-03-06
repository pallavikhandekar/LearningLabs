"""

Django settings for LearningLabs project.



For more information on this file, see

https://docs.djangoproject.com/en/1.6/topics/settings/



For the full list of settings and their values, see

https://docs.djangoproject.com/en/1.6/ref/settings/

"""



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))





# Quick-start development settings - unsuitable for production

# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/



# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = '1x74#-pmjp6u=5o+bs&p-#yvy!)k9-5z$(gp3+ol^uyn^=k9j7'



# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True



TEMPLATE_DEBUG = True



ALLOWED_HOSTS = []





# Application definition



INSTALLED_APPS = (

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    'mongoengine.django.mongo_auth',

    'django_tables2',

)











MIDDLEWARE_CLASSES = (

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)



ROOT_URLCONF = 'LearningLabs.urls'



WSGI_APPLICATION = 'LearningLabs.wsgi.application'



AUTHENTICATION_BACKENDS = (

    'mongoengine.django.auth.MongoEngineBackend',

)



# Database

# https://docs.djangoproject.com/en/1.6/ref/settings/#databases



DATABASES = {

    'default' : {

      'ENGINE' : 'django_mongodb_engine',

      'NAME' : 'my_database'

   }

}



STATIC_URL = '/static/'



STATICFILES_DIRS = (

    "./static",            

)



TEMPLATE_DIRS = (

    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".

    #"C:/Users/dgada/workspace/git/Peg-a-Page/Templates"

#     "./Templates"

    "./Templates"

    # Always use forward slashes, even on Windows.

    # Don't forget to use absolute paths, not relative paths.

)



TEMPLATE_CONTEXT_PROCESSORS = (

 'django.core.context_processors.request',                              

 'django.contrib.auth.context_processors.auth',

)

# Internationalization

# https://docs.djangoproject.com/en/1.6/topics/i18n/



LANGUAGE_CODE = 'en-us'



TIME_ZONE = 'UTC'



USE_I18N = True



USE_L10N = True



USE_TZ = True





# Static files (CSS, JavaScript, Images)

# https://docs.djangoproject.com/en/1.6/howto/static-files/

