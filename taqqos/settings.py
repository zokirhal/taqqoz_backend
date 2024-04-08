import os
import environ
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ["*"]

ENVIRONMENT = env("ENVIRONMENT", default="DEV")


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # installed apps
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'phonenumber_field',
    'parler',
    'ckeditor_uploader',
    'ckeditor',
    'rest_framework_simplejwt.token_blacklist',
    'django_celery_results',
    'smart_selects',
    "django_celery_beat",

    # django apps
    'taqqos.account',
    'taqqos.core',
    'taqqos.document',
    'taqqos.geo',
    'taqqos.product',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'taqqos.core.middlewares.SetLanguageMiddleware',
]

ROOT_URLCONF = 'taqqos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'taqqos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_DATABASE"),
        "USER": env("DB_USERNAME"),
        "PASSWORD": env("DB_USER_PASSWORD"),
        "HOST": env("DB_HOSTNAME"),
        "PORT": env("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGES = (
    ("ru", "Russian"),
    ("uz", "Uzbek"),
    # ("en", "English")
)

PARLER_DEFAULT_LANGUAGE_CODE = 'ru'

PARLER_LANGUAGES = {
    None: (
        {'code': 'uz', },
        {'code': 'ru', },
        # {'code': 'en', },
    ),
    'default': {
        'fallback': 'ru',
        'hide_untranslated': False,
        # the default; let .active_translations() return fallbacks too.
    }
}
PARLER_ENABLE_CACHING = False

PARLER_DEFAULT_ACTIVATE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "account.User"

SMS_GATEWAY_WITH_PLAY_MARKET = {
    "BASE_URL": env("PLAY_SMS_BASE_URL", default=""),
    "LOGIN": env("PLAY_SMS_LOGIN", default=""),
    "PASSWORD": env("PLAY_SMS_PASSWORD", default=""),
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'apps.gauth.authentication.FirebaseAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'taqqos.core.pagination.Pagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'ALLOWED_VERSIONS': (None, 'v1', 'v2', 'v3')
}

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
SMS_CODE_EXPIRE = 60

SIMPLE_JWT = {
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CORS_ALLOW_ALL_ORIGINS = True

DEMO_ACCOUNT_CODE = env("DEMO_ACCOUNT_CODE", default=4444)

CKEDITOR_UPLOAD_PATH = "uploads/"

from taqqos.jazzmin_settings import *


ADMIN_ORDERING = (
    ("account", ("User", )),
    ("document", ("File", )),
    ("auth", ("Group",)),
    ("product", (
        "Category",
        "Brand",
        "Attribute",
        "Product",
        "ProductPrice",
        "Review",
        "Favourite",
        "Slider",
        "Seller")
     ),
)

REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")

CELERY_RESULT_BACKEND = "django-db"

CELERY_BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_EAGER = True
CELERY_ALWAYS_EAGER = True
