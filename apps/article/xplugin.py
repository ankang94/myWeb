from django.template import loader
from xadmin.views import BaseAdminPlugin
from xadmin.plugins.utils import get_context_dict
from myWeb.adapter import Cache


class RefreshButton(BaseAdminPlugin):
    refresh_cache_plugin = False

    def init_request(self, *args, **kwargs):
        return self.refresh_cache_plugin

    def block_top_navmenu(self, context, nodes):
        if self.refresh_cache_plugin:
            content = {'refresh': [{'name': '导航栏', 'val': '1'},
                                   {'name': '轮播图', 'val': '2'},
                                   {'name': '右侧图', 'val': '3'},
                                   {'name': '排行', 'val': '4'},
                                   {'name': '所有', 'val': '5'}]}
            context.update(content)
            nodes.append(
                loader.render_to_string('xadmin/blocks/common.top.refresh.html',
                                        get_context_dict(context))
            )


class RefreshPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        data = self.request.POST.get('REFRESH_DATA')
        if data in [str(x) for x in range(1, 6)]:
            Cache().remove({'1': 'titles',
                            '2': 'carousel',
                            '3': 'adpic',
                            '4': 'tops',
                            '5': None}.get(data))
        return False
