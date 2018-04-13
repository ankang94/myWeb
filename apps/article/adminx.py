# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

import os
from django.conf import settings
import xadmin
from xadmin import views
from apps.article.models import Article, ArticleGroup, Script, Image, ExtSource
from xadmin.views import ListAdminView
from .xplugin import CachePlugin


# 基本的修改
class BaseSetting(object):
    enable_themes = True  # 打开主题功能
    use_bootswatch = True  #


class GlobalSetting(object):
    site_title = u'安康云'
    site_footer = u'安康云'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)


class ArticleAdmin(object):
    list_display = ['title', 'group', 'comment', 'script', 'image', 'createdate']
    list_editable = ['group']
    list_filter = ('group', 'createdate')
    search_fields = ('title', 'comment')
    model_icon = 'fa fa-hdd-o'


class ArticleGroupAdmin(object):
    list_display = ['groupid', 'comment']
    model_icon = 'fa fa-clone'
    refresh_cache_plugin = True


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
    refresh_cache_plugin = True

    def delete_model(self):
        self.log('delete', '', self.obj)
        self.obj.delete()
        file = os.path.join(settings.MEDIA_ROOT, 'ext', self.obj.path.url.split('/')[-1])
        if os.path.exists(file):
            os.remove(file)


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(ArticleGroup, ArticleGroupAdmin)
xadmin.site.register(Script, ScriptAdmin)
xadmin.site.register(Image, ImageAdmin)
xadmin.site.register(ExtSource, ExtSourceAdmin)

xadmin.site.register_plugin(CachePlugin, ListAdminView)