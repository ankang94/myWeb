# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/5/7 上午 10:58'

from django.conf.urls import url
from clone.views import test_index

app_name = 'clone'

urlpatterns = [
    url(r'^test$', test_index, name='get_task_list'),
]
