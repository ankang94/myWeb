# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

import os
from django.conf import settings
from xadmin.sites import site
from xadmin.views import BaseAdminView, CommAdminView
from apps.article.models import Article, ArticleGroup, Script, Image, ExtSource
from .xplugin import RefreshButton, RefreshPlugin


# 基本的修改
class BaseSetting(object):
    enable_themes = True  # 打开主题功能
    use_bootswatch = True  #
    refresh_cache_plugin = True


class GlobalSetting(object):
    site_title = u'安康云'
    site_footer = u'安康云'


site.register(BaseAdminView, BaseSetting)
site.register(CommAdminView, GlobalSetting)


class ArticleAdmin(object):
    list_display = ['title', 'group', 'comment', 'script', 'image', 'createdate']
    list_editable = ['group']
    list_filter = ('group', 'createdate')
    search_fields = ('title', 'comment')
    model_icon = 'fa fa-hdd-o'


class ArticleGroupAdmin(object):
    list_display = ['groupid', 'comment']
    model_icon = 'fa fa-clone'


class ScriptAdmin(object):
    list_display = ['name', 'type', 'path']
    model_icon = 'fa fa-file-code-o'


class ImageAdmin(object):
    list_display = ['name', 'rel_img_name', 'path']
    model_icon = 'fa fa-file-image-o'

    def delete_model(self):
        self.log('delete', '', self.obj)
        self.obj.delete()
        file = os.path.join(settings.MEDIA_ROOT, 'img', self.obj.path.url.split('/')[-1])
        if os.path.exists(file):
            os.remove(file)


class ExtSourceAdmin(object):
    list_display = ['title', 'rel_img_name', 'type', 'state', 'seq']
    model_icon = 'fa fa-object-group'
    ordering = ['type', 'seq']

    def delete_model(self):
        self.log('delete', '', self.obj)
        self.obj.delete()
        file = os.path.join(settings.MEDIA_ROOT, 'ext', self.obj.path.url.split('/')[-1])
        if os.path.exists(file):
            os.remove(file)


site.register(Article, ArticleAdmin)
site.register(ArticleGroup, ArticleGroupAdmin)
site.register(Script, ScriptAdmin)
site.register(Image, ImageAdmin)
site.register(ExtSource, ExtSourceAdmin)

site.register_plugin(RefreshButton, BaseAdminView)
site.register_plugin(RefreshPlugin, BaseAdminView)
