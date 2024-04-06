import os
from pathlib import Path
from django.urls import reverse_lazy
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'chronicled',
    'chronicled.profiles',
    'chronicled.common',
    'chronicled.games',

    'fontawesomefree',
]

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

ROOT_URLCONF = 'chronicled.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'chronicled.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'chronicled.wsgi.application'

database_url = os.environ.get("DATABASE_URL")

DATABASES = {
    'default': dj_database_url.config(
        default=database_url,
        conn_max_age=600,
    )
}


# DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": "chronicle-db",
#             "USER": "postgres",
#             "PASSWORD": "password",
#             "HOST": "127.0.0.1",
#             "PORT": "5432",
#         }
#     }

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

TIME_ZONE = 'Europe/Sofia'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'mediafiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'profiles.AppUser'

LOGIN_REDIRECT_URL = reverse_lazy('home-page')

LOGOUT_REDIRECT_URL = reverse_lazy('login')

LOGIN_URL = 'login'

CSRF_TRUSTED_ORIGINS = ['https://www.chronicled.krasye.com', 'https://chronicled.krasye.com']
