from .common import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'site7',
        'USER': 'kmglocal',
        'PASSWORD': '1234',
        'HOST': '172.17.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # 추가, 만약에 이 부분 때문에 오류가 난다면, 이 라인을 지우고 다시 시도해주세요.
        },
    }
}