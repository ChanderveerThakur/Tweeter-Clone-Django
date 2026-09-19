"""
Django settings for tweeter project configured with MongoDB and ImageKit.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from both project folder and workspace root
load_dotenv(BASE_DIR / '.env')
load_dotenv(BASE_DIR.parent / '.env')

# SECURITY
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-tweeter-key-for-dev-environment-change-in-prod')
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't', 'yes')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
    '*',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
if extra_csrf := os.getenv('CSRF_TRUSTED_ORIGINS'):
    CSRF_TRUSTED_ORIGINS.extend([origin.strip() for origin in extra_csrf.split(',') if origin.strip()])

# DATABASE SELECTION & APPS CONFIGURATION
USE_SQLITE = os.getenv('USE_SQLITE', 'False').lower() in ('true', '1')

if USE_SQLITE:
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'tweet',
    ]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
else:
    INSTALLED_APPS = [
        'tweeter.apps.MongoAdminConfig',
        'tweeter.apps.MongoAuthConfig',
        'tweeter.apps.MongoContentTypesConfig',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'tweet',
    ]
    MONGODB_URI = os.getenv('MONGODB_URI') or os.getenv('MONGODB_HOST', 'mongodb://localhost:27017/')
    MONGODB_NAME = os.getenv('MONGODB_NAME', 'tweeter_db')

    DATABASES = {
        'default': {
            'ENGINE': 'django_mongodb_backend',
            'HOST': MONGODB_URI,
            'NAME': MONGODB_NAME,
            'OPTIONS': {
                'serverSelectionTimeoutMS': 3000,
            },
        }
    }
    DATABASE_ROUTERS = ["django_mongodb_backend.routers.MongoRouter"]
    DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'
    MIGRATION_MODULES = {
        'admin': 'mongo_migrations.admin',
        'auth': 'mongo_migrations.auth',
        'contenttypes': 'mongo_migrations.contenttypes',
    }

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tweeter.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tweeter.wsgi.application'

# IMAGEKIT CLOUD STORAGE
IMAGEKIT_PUBLIC_KEY = os.getenv('IMAGEKIT_PUBLIC_KEY', '')
IMAGEKIT_PRIVATE_KEY = os.getenv('IMAGEKIT_PRIVATE_KEY', '')
IMAGEKIT_URL_ENDPOINT = os.getenv('IMAGEKIT_URL_ENDPOINT', '')

# PASSWORD VALIDATION
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

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# AUTHENTICATION
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
