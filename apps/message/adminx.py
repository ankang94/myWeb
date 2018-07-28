# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

from xadmin.sites import site
from apps.message.models import Visitor, Message


class VisitorAdmin(object):
    list_display = ['name', 'email', 'ban', 'date']
    list_editable = ['ban', 'date']
    list_filter = ('ban', 'date')
    search_fields = ('name', 'email', 'date')
    model_icon = 'fa fa-address-book-o'


class MessageAdmin(object):
    list_display = ['visitor', 'article', 'message', 'date']
    list_editable = ['message', 'date']
    list_filter = ('visitor__name', 'article__title', 'date')
    model_icon = 'fa fa-commenting-o'


site.register(Visitor, VisitorAdmin)
site.register(Message, MessageAdmin)
