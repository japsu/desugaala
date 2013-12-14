# Django settings for desugaala project.

import dj_database_url
import os

def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *parts))

DEMO_MODE = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {}
DATABASES['default'] = dj_database_url.config() if 'DATABASE_URL' in os.environ else {
    'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'desugaala.sqlite3',                      # Or path to database file if using sqlite3.
    'USER': '',                      # Not used with sqlite3.
    'PASSWORD': '',                  # Not used with sqlite3.
    'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Helsinki'
DATETIME_FORMAT = 'd.m.y H:i'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fi'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = mkpath('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    mkpath('bower_components'),
)

STATICFILES_FINDERS = (
    'pipeline.finders.FileSystemFinder',
    'pipeline.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'pipeline.finders.CachedFileFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i#q-%)p%=nsewazxrfi9@98!%(e$tdy%d6=jdie=%y7o1lan*('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'desugaala.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'desugaala.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'pipeline',
    'gunicorn',
    'south',
    'vote',
    'status'
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
  'pipeline.compilers.coffee.CoffeeScriptCompiler',
)

PIPELINE_COFFEE_SCRIPT_BINARY = 'coffee' # hail PATH

PIPELINE_JS = {
    'default': {
        'source_filenames': (
            'jquery/jquery.min.js',
            'jqueryui/ui/minified/jquery.ui.core.min.js',
            'jqueryui/ui/minified/jquery.ui.widget.min.js',
            'jqueryui/ui/minified/jquery.ui.mouse.min.js',
            'jqueryui/ui/minified/jquery.ui.sortable.min.js',
            'jqueryui/ui/minified/jquery.ui.draggable.min.js',
            'bacon/dist/Bacon.min.js',
            'bacon.jquery/dist/bacon.jquery.min.js',
            'bootstrap/dist/js/bootstrap.min.js',
            'js/desugaala.coffee',
        ),
        'output_filename': 'js/desugaala.js',
    }
}

PIPELINE_CSS = {
    'default': {
        'source_filenames': (
            'bootstrap/dist/css/bootstrap.min.css',
            'css/desugaala.css',
        ),
        'output_filename': 'css/desugaala.css'
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# production only
PHPBB_AUTH_DB_MODULE = "MySQLdb"
PHPBB_AUTH_DB_PARAMS = {
   "host":      "",
   "user":      "",
   "passwd":    "", # some libs use key "password"
   "db":        "", # some libs use key "database"
}
PHPBB_AUTH_DB_PARAM_STYLE = "%s"
PHPBB_AUTH_DB_USERS_TABLE = "users"

GOOGLE_ANALYTICS_TOKEN = '0000000-0'
