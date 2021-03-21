ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dj_diplom',
        'USER': 'nikita',
        'PASSWORD': 'pass',
        'HOST': 'localhost',
        'PORT': '',
    }
}
