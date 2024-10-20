# settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'your_secret_key_here'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customer',  
    'neograph',
    'django_neomodel',
    'django_extensions',
    'celery',
    'django_celery_beat',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dj_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add your project-level templates directory here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dj_proj.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'customer:login'  # Assuming you have a URL named 'login' in your 'customer' app
LOGIN_REDIRECT_URL = 'customer:index'  # Redirect to 'index' view after login
LOGOUT_REDIRECT_URL = 'customer:login'

# Neomodel configuration
NEOMODEL_NEO4J_BOLT_USER  = os.getenv('NEO_USER','neo4j')
NEOMODEL_NEO4J_BOLT_PASSWORD  = os.getenv('NEO_PWD',None)
NEO_SERVER = os.getenv('NEO_SERVER',None)
NEO_PORT = os.getenv('NEO_PORT','7687')
NEOMODEL_NEO4J_BOLT_URL_API = None
NEOMODEL_NEO4J_BOLT_URL = None
NEO_NEO4J_AUTH = None


if not NEO_SERVER:
    raise ValueError('NEO4j server is not configured')
if not NEOMODEL_NEO4J_BOLT_PASSWORD:
    raise ValueError('NEO4J password is not configured')
if NEO_SERVER and NEOMODEL_NEO4J_BOLT_PASSWORD :
    NEOMODEL_NEO4J_BOLT_URL = f'bolt://{NEOMODEL_NEO4J_BOLT_USER }:{NEOMODEL_NEO4J_BOLT_PASSWORD }@{NEO_SERVER}:{NEO_PORT}'
    NEOMODEL_NEO4J_BOLT_URL_API = f'bolt://{NEO_SERVER}:{NEO_PORT}'
    NEO_NEO4J_AUTH = (NEOMODEL_NEO4J_BOLT_USER ,NEOMODEL_NEO4J_BOLT_PASSWORD )

NEOMODEL_ENCRYPTED_CONNECTION = False
NEOMODEL_SIGNALS = True 

# settings for celery

CELERY_BROKER_URL = 'pyamqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'rpc://'

# logging
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')  # Specify the directory where logs will be stored
# Ensure the 'logs' directory exists, create it if it doesn't
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'dj_proj': {  # Specify your app name here
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}




