# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/26 22:29'

import xadmin
from xadmin import views


class GlobalSetting(object):
    site_title = u'安康云'
    site_footer = u'安康云'


xadmin.site.register(views.CommAdminView, GlobalSetting)
