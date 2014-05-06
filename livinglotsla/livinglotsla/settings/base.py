from collections import OrderedDict
import os
from os.path import abspath, dirname

from django.core.exceptions import ImproperlyConfigured

# TODO document required environment variables

ENV_VARIABLE_PREFIX = 'LAOA'

def get_env_variable(var_name, optional=False):
    """Get the environment variable or return exception"""
    if not ENV_VARIABLE_PREFIX:
        raise ImproperlyConfigured('Set ENV_VARIABLE_PREFIX')
    try:
        return os.environ[ENV_VARIABLE_PREFIX + '_' + var_name]
    except KeyError:
        if optional:
            return None
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)


DATABASES = {
    'default': {
        # > createdb -T template_postgis livinglotsla
        # > psql
        # # create user livinglotsla with password 'password';
        # # grant all privileges on database livinglotsla to
        # livinglotsla;
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
    }
}

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
)

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = 'America/New_York'

PROJECT_ROOT = os.path.join(abspath(dirname(__file__)), '..', '..')

DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = get_env_variable('SECRET_KEY')

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
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'honeypot.middleware.HoneypotMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'watson.middleware.SearchContextMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',

    'feincms.context_processors.add_page_if_missing',
)

ROOT_URLCONF = 'livinglotsla.urls'

WSGI_APPLICATION = 'livinglotsla.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    #
    # django contrib
    #
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',

    #
    # third-party
    #
    'actstream',
    'admin_enhancer',
    'autocomplete_light',
    'compressor',
    'contact_form',
    'django_monitor',
    'djangojs',
    'feincms',
    'feincms.module.medialibrary',
    'feincms.module.page',
    'flatblocks',
    'honeypot',
    'imagekit',
    'inplace',
    'inplace.boundaries',
    'jsonfield',
    'mptt',
    'reversion',
    'reversion_compare',
    'south',
    'watson',
    'widget_tweaks',

    #
    # first-party, project-generic
    #
    'cartodbsync',
    'external_data_sync',
    'inplace_activity_stream',
    'pagepermissions',
    'rsssync',
    'search',

    #
    # Living Lots
    #
    'livinglots_activities',
    'livinglots_friendlyowners',
    'livinglots_lots',
    'livinglots_mailings',
    'livinglots_notify',
    'livinglots_organize',
    'livinglots_owners',
    'livinglots_pathways',
    'livinglots_steward',
    'livinglots_usercontent.files',
    'livinglots_usercontent.notes',
    'livinglots_usercontent.photos',

    #
    # first-party, project-specific
    #
    'activity_stream',
    'cms',
    'contact',
    'datasync',
    'export',
    'friendlyowners',
    'groundtruth',
    'lots',
    'lotfinders',
    'mailings',
    'organize',
    'owners',
    'pathways',
    'steward',
    'usercontent',

    'ladata',
    'ladata.buildings',
    'ladata.communityplanareas',
    'ladata.councildistricts',
    'ladata.localroll',
    'ladata.neighborhoodcouncils',
    'ladata.parcels',
    'ladata.protectedareas',
    'ladata.sidelots',
    'ladata.transmissionlines',
    'ladata.weedabatements',
    'ladata.zoning',
)

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
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

PLACES_MAPBOX_ID = 'laopenacres.i370m24m'

SOUTH_TESTS_MIGRATE = False

RECAPTCHA_PRIVATE_KEY = get_env_variable('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = get_env_variable('RECAPTCHA_PUBLIC_KEY')

ORGANIZE_PARTICIPANT_SALT = get_env_variable('ORGANIZE_PARTICIPANT_SALT')

ACTSTREAM_SETTINGS = {
    'MANAGER': 'inplace_activity_stream.managers.PlaceActionManager',
    'MODELS': (
        'auth.user',
        'files.file',
        'lots.lot',
        'notes.note',
        'organize.organizer',
        'photos.photo',
    ),
    'USE_JSONFIELD': True,
}
ACTIVITY_STREAM_DEFAULT_ACTOR_PK = get_env_variable('ACTSTREAM_DEFAULT_ACTOR_PK')

FACILITATORS = {
    'global': [],
}

EMAIL_SUBJECT_PREFIX = '[LA Open Acres] '

MAILREADER_REPLY_PREFIX = 'Reply with text above this line to post a public note.'
MAILREADER_IGNORE_FROM = []
MAILREADER_HOST = get_env_variable('MAILREADER_HOST')
MAILREADER_HOST_USER = get_env_variable('MAILREADER_HOST_USER')
MAILREADER_HOST_PASSWORD = get_env_variable('MAILREADER_HOST_PASSWORD')

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_richtext.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + 'bower_components/tinymce/js/tinymce/tinymce.js',
}

SOUTH_MIGRATION_MODULES = {
    'page': 'cms.migrate.page',
    'medialibrary': 'cms.migrate.medialibrary',
}

HONEYPOT_FIELD_NAME = 'homepage_url'
HONEYPOT_VALUE = 'http://example.com/'

ADMIN_TOOLS_INDEX_DASHBOARD = 'livinglotsla.admindashboard.LivingLotsDashboard'

LIVING_LOTS = {
    'MODELS': {
        'lot': 'lots.Lot',
        'lotgroup': 'lots.LotGroup',
        'lotlayer': 'lots.LotLayer',
        'organizer': 'organize.Organizer',
        'owner': 'owners.Owner',
        'pathway': 'pathways.Pathway',
        'parcel': 'parcels.Parcel',
        'stewardproject': 'steward.StewardProject',
    },
}

LOCAL_PROJECTION = 2229

LADATA_PARCEL_VIEWER_URL = 'http://maps.assessor.lacounty.gov/mapping/rolldata.asp?ain='
LADATA_PROCESSED_DATA_DIR = get_env_variable('LADATA_PROCESSED_DATA_DIR',
                                             optional=True)
LADATA_UA = ('Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 '
             '(KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')

CONTACT_FORM_REASONS = OrderedDict([
    ('The lot I want permission to use is not here.', ['hello@laopenacres.org',]),
    ('I want to share my land access story.', ['hello@laopenacres.org',]),
    ('I want to loan or lease my land for a temporary project.', ['hello@laopenacres.org',]),
    ('I want to invite admins to an event.', ['hello@laopenacres.org',]),
    ('I have a press inquiry.', ['hello@laopenacres.org',]),
])


CARTODB_SYNC = {
    'API_KEY': get_env_variable('CARTODBSYNC_API_KEY'),
    'DOMAIN': get_env_variable('CARTODBSYNC_DOMAIN'),
    'MODELS': [
        {
            'CARTODB_TABLE': get_env_variable('CARTODBSYNC_LOTS_TABLE'),
            'MODEL_CLASS': 'lots.Lot',
            'SYNCHRONIZER_CLASS': 'lots.cartodbsynchronizers.LotSynchronizer',
        }
    ]
}
