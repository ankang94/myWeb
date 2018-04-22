2018-03-27 09:06
my first web project used django version 1.11

2018-04-22 15:59
modify setting.py devide connection info

vim base.py
========================================================================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库',
        'USER': '用户名',
        'PASSWORD': '密码',
        'HOST': '数据库地址',
        'PORT': '3306',
        'OPTIONS': {
            # 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://Redis地址:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "密码"
        },
    }
}
========================================================================================================================
