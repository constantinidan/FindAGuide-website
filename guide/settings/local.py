"""
Django settings for myproj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django.conf.global_settings as DEFAULT_SETTINGS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b0(7=s+^7f)7#8&$+8#!$220989rse5rny3anwm1e$!1p(!(l*'

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
    'south',
    'sendgrid',
    'Profile',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'guide.middleware.ReferMiddleware',

)

ROOT_URLCONF = 'guide.urls'

WSGI_APPLICATION = 'guide.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SHARE_URL = "http://127.0.0.1:8000/?ref="


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    #BASE_DIR + '/templates/',
    #/Users/danconstantini/miniconda3/envs/myenv/myproj,
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'   #It's the name that's showed when inspecting the elmt

#STATIC_ROOT = '/Users/danconstantini/miniconda3/envs/myenv/src/static/static_root/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static_root') 

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'static_dirs'), 
    #'/Users/danconstantini/miniconda3/envs/myenv/src/static/static_dirs/',# add im, css
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
#MEDIA_ROOT = '/Users/danconstantini/miniconda3/envs/myenv/src/static/media/'

MEDIA_URL = '/media/'


#DO python manage.py collectstatic for collecting static after import.

