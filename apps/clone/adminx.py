# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

from apps.clone.models import CopyArticle, CopyLogin
from apps.clone.views import CloneArticle
from xadmin.sites import site
from xadmin.views import BaseAdminView
from .xplugin import CopyPlugin


class CopyArticleAdmin(object):
    list_display = ['name', 'host', 'title', 'h2', 'h3', 'context', 'code', 'exclude']
    list_editable = ['name', 'host', 'title', 'h2', 'h3', 'context', 'code', 'exclude']
    model_icon = 'fa fa-building-o'


class CopyLoginAdmin(object):
    list_display = ['host', 'username', 'password', 'signal', 'cookie', 'js']
    list_editable = ['username', 'password', 'signal', 'cookie']
    model_icon = 'fa fa-rocket'


site.register(CopyArticle, CopyArticleAdmin)
site.register(CopyLogin, CopyLoginAdmin)
site.register_plugin(CopyPlugin, BaseAdminView)
site.register_view(r'copy-article/$', CloneArticle, name='get_task_list')

