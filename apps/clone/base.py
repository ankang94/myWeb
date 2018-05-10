# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/5/7 上午 9:29'

import os
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

COOKIE_DIR = os.path.join(settings.BASE_DIR, 'apps', 'clone', 'cookies')


class Config:
    args = None
    user_data = None
    user_crx = None

    def __init__(self, param):
        self.args = param.get('args')
        self.user_data = param.get('user_data')
        self.user_crx = param.get('user_crx')


class SelfException(Exception):
    pass


def create_entry(dynamic=False, config=None, *clzz):
    cls = DynamicEntry if dynamic else StaticEntry

    class Entry(*clzz, cls):
        def __init__(self):
            super(clzz[-1], self).__init__(config)

    return Entry()


class DynamicEntry:
    def __init__(self, config=None):
        self.args = config.args
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        if config and config.user_data:
            chrome_options.add_argument('--user-data-dir=' + config.user_data)  # 设置成用户
        if config and config.user_crx:
            chrome_options.add_extension(config.user_crx)  # 自己下载的crx路径'd:\crx\AdBlock_v2.17.crx'
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def perform(self):
        raise SelfException('no excute script found.')

    def start(self):
        try:
            return self.perform()
        except Exception as e:
            if isinstance(e, SelfException):
                print('get web content fail.')
            else:
                raise e
            return None
        finally:
            self.driver.close()


class StaticEntry:
    def __init__(self, config=None):
        self.args = config.args

    def perform(self):
        raise SelfException('no excute script found.')

    def start(self):
        pass
