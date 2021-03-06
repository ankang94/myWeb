# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/5/7 下午 4:37'

from enum import Enum, unique


class Cache(object):
    from django.core.cache import cache as redis_cache
    from django_redis import get_redis_connection
    cache = redis_cache
    clear_redis = get_redis_connection("default")
    __instance = None

    def get(self, key):
        return self.cache.get(key)

    def remove(self, key=None):
        if key:
            if self.cache.keys(key):
                self.cache.delete_pattern(key)
        else:
            self.clear_redis.flushall()

    def __init__(self, key=None, value=None, timeout=None):
        if key and value:
            self.cache.set(key, value, timeout)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance


@unique
class Method(Enum):
    GET = 'GET'
    POST = 'POST'


class Ajax(object):

    @staticmethod
    def connect(url, method, param):
        import requests
        import json
        from django.conf import settings

        config = settings.AJAX.get("default")

        url = config.get("URL") + url
        headers = config.get("HEADERS")

        response = requests.request(method.value, url, headers=headers, params=param)

        return json.loads(response.text)
