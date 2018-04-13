# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

import xadmin
from xadmin import views
from xadmin.plugins.actions import BaseActionView
# from django.http import HttpResponse
from apps.article.models import Article, ArticleGroup, Script, Image, ExtSource
from article.utils import Cache


class DelCacheAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "refresh"  #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'clear cache'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'  #: 该 Action 所需权限

    # 而后实现 do_action 方法
    def do_action(self, queryset):
        Cache().remove()
        # queryset 是包含了已经选择的数据的 queryset
        # for obj in queryset:
            # obj 的操作
            # ...
        # 返回 HttpResponse
        # return HttpResponse('refresh success')


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
    model_icon = 'fa fa-hdd-o'
    actions = [DelCacheAction, ]


class ArticleGroupAdmin(object):
    model_icon = 'fa fa-clone'
    actions = [DelCacheAction, ]


class ScriptAdmin(object):
    model_icon = 'fa fa-file-code-o'


class ImageAdmin(object):
    model_icon = 'fa fa-file-image-o'


class ExtSourceAdmin(object):
    model_icon = 'fa fa-object-group'
    actions = [DelCacheAction, ]


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(ArticleGroup, ArticleGroupAdmin)
xadmin.site.register(Script, ScriptAdmin)
xadmin.site.register(Image, ImageAdmin)
xadmin.site.register(ExtSource, ExtSourceAdmin)
