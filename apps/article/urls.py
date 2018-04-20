# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/4/18 15:39'

from django.conf.urls import url
from article.views import article, catlog, search

app_name = 'article'

urlpatterns = [
    url(r'^(g(?P<gid>\d*)/)?(p(?P<pid>\d*))?$', catlog),
    url(r'^g(?P<gid>\d+)/a(?P<aid>\d+)', article),
    url(r'^search(/p(?P<pid>\d*))?$', search, name='search'),
]