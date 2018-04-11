# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

import xadmin
from xadmin import views
from .models import Article, ArticleGroup, Script, Image


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
    list_editable = ['group']
    list_filter = ('group', 'createdate')
    search_fields = ('title', 'comment')
    model_icon = 'fa fa-folder-open'


class ArticleGroupAdmin(object):
    model_icon = 'fa fa-cubes'
    pass


class ScriptAdmin(object):
    model_icon = 'fa fa-file-code-o'
    pass


class ImageAdmin(object):
    model_icon = 'fa fa-file-image-o'
    pass


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(ArticleGroup, ArticleGroupAdmin)
xadmin.site.register(Script, ScriptAdmin)
xadmin.site.register(Image, ImageAdmin)
