# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

from xadmin.sites import site
from apps.clone.models import CopyArticle


class CopyArticleAdmin(object):
    list_display = ['name', 'host', 'shost', 'title', 'h2', 'h3', 'context', 'code']
    list_editable = ['name', 'host', 'shost', 'title', 'h2', 'h3', 'context', 'code']
    model_icon = 'fa fa-building-o'


site.register(CopyArticle, CopyArticleAdmin)
