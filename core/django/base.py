from pathlib import Path
from datetime import timedelta
from core.env import BASE_DIR, env

env.read_env(str(BASE_DIR / '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG')

ALLOWED_HOSTS = ['*']

# public apps
SHARED_APPS = (
    'django_tenants',
    'users', # superuser app
    'apps.school',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_extensions',
)

TENANT_APPS = (
    'apps.teacher',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
PUBLIC_SCHEMA_URLCONF = "users.urls_public"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # "ROTATE_REFRESH_TOKENS": True,
    # "BLACKLIST_AFTER_ROTATION": True,
}

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str('POSTGRES_TENANTS_ENGINE'),
        'NAME': env.str('POSTGRESQL_DATABASE_NAME'),
        'USER': env('POSTGRESQL_USER'),
        'PASSWORD': env.str('POSTGRESQL_PASSWORD'),
        'HOST': env.str('POSTGRESQL_HOSTNAME'),
        'PORT': env.int('POSTGRESQL_PORT'),
    }
}

DATABASE_ROUTERS = (
    env.str('DJANGO_TENANT_DATABASE_ROUTERS'),
)


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

TIME_ZONE = 'Asia/Karachi'

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_DIRS = [
    Path().joinpath(BASE_DIR, 'static')
]

STATIC_URL = 'static/'

# Media files settings
MEDIA_URL = '/media/'

MEDIA_ROOT = Path().joinpath(BASE_DIR, 'media/')

MULTITENANT_RELATIVE_MEDIA_ROOT = 'tenants/%s'

TENANT_MODEL = env.str("DJANGO_TENANT_MODEL")
TENANT_DOMAIN_MODEL = env.str("DJANGO_TENANT_DOMAIN_MODEL")
SHOW_PUBLIC_IF_NO_TENANT_FOUND = env.bool("SHOW_PUBLIC_IF_NO_TENANT_FOUND")

AUTH_USER_MODEL = 'users.CustomUser'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
from core.settings.s3_storage import * # noqa
from core.settings.cors import *  # noqa
from core.settings.sessions import *  # noqa
from core.settings.celery import *  # noqa
from core.settings.sentry import *  # noqa

"""
