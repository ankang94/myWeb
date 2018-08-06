# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

from xadmin.sites import site
from xadmin.plugins.actions import DeleteSelectedAction
from apps.message.models import Visitor, Message
from myWeb.adapter import Ajax, Method


class RefreshAction(DeleteSelectedAction):
    def delete_models(self, queryset):
        articles = []
        for obj in queryset:
            articles.append(str(obj.article.articleid))
        super().delete_models(queryset)
        Ajax.connect('/message/refresh', Method.POST, {'articles': ','.join(articles)})


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
    actions = [RefreshAction, ]

    def delete_model(self):
        self.log('delete', '', self.obj)
        self.obj.delete()
        Ajax.connect('/message/refresh', Method.POST,
                     {'articles': str(self.obj.article.articleid)})


site.register(Visitor, VisitorAdmin)
site.register(Message, MessageAdmin)
