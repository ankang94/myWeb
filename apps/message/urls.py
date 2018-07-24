# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/7/23 10:44'

from django.conf.urls import url
from message.views import message_list, message_add

app_name = 'msg_board'


urlpatterns = [
    url(r'^message_board/list', message_list, name='list'),
    url(r'^message_board/add$', message_add, name='add')
]
