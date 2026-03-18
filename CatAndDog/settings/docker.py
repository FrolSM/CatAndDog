from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES['default']['HOST'] = 'db'
DATABASES['default']['PORT'] = 5432

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX':'redis_cache'
    }
}
