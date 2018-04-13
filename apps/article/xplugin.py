# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

from django.template import loader
from xadmin.views import BaseAdminPlugin

from article.utils import Cache


class CachePlugin(BaseAdminPlugin):
    refresh_cache_plugin = False

    def init_request(self, *args, **kwargs):
        return self.refresh_cache_plugin

    def block_nav_menu(self, __, nodes):
        if self.refresh_cache_plugin:
            # name = self.request.path.strip('/').split('/')[-1]
            Cache().remove()
            context = {'about_content': u'清理缓存成功'}
        nodes.append(
            loader.render_to_string('xadmin/blocks/model_list.nav_menu.refreshcache.html', context)
        )
