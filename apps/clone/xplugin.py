# -*- coding: utf-8 -*-
from django.template import loader

from clone.views import *
from xadmin.plugins.utils import get_context_dict
from xadmin.views import BaseAdminPlugin


class CopyPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return self.request.path == '/adminarticle/article/'

    def block_nav_form(self, context, nodes):
        content = {'ret': init_clone_template, 'btn_name': '拷贝 文章库'}
        context.update(content)

        nodes.append(
            loader.render_to_string('xadmin/blocks/moal_list.nav_menu.clone.html',
                                    get_context_dict(context))
        )
