# Django settings for django-rest-utils project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['*']

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-uk'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_URL = '/static/'
STATIC_ROOT = ''

SECRET_KEY = 'u@x-aj9(hoh#rb-^ymf#g2jx_hp0vj7u5#b@ag1n^seu9e!%cy'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
)

AUTH_USER_MODEL = 'auth.User'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-fixture-bundling', '--logging-filter=-south']
