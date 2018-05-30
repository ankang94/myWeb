# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/5/7 上午 9:29'

import os
import pickle

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

COOKIE_DIR = os.path.join(settings.BASE_DIR, 'apps', 'clone', 'cookies')


class Config:
    args = None
    user_data = None
    user_crx = None
    cookie_path = None
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:49.0) Gecko/20100101 Firefox/49.0',
    }

    def __init__(self, param):
        self.args = param.get('args')
        self.user_data = param.get('user_data')
        self.user_crx = param.get('user_crx')
        self.url = param.get('url')
        self.cookie_path = param.get('cookie')
        self.headers = self.header.update(param.get('headers')) if param.get('headers') else self.header


def create_soup(config=None, *clzz):
    from itertools import chain

    class LoginEntry(*chain(clzz, (Entry,))):
        def __init__(self):
            super(clzz[-1], self).__init__(config)

    conn = requests.session()
    conn.headers = config.headers
    conn.verify = False
    target_html = conn.get(config.url)
    if config.url != target_html.url:
        jar = RequestsCookieJar()
        if os.path.exists(config.cookie_path):
            load_cookie(config.cookie_path, jar)
            # 添加session再次访问
            target_html = conn.get(config.url, cookies=jar)
            # 重定向重新获取session
            if config.url != target_html.url:
                LoginEntry().start()
                jar = RequestsCookieJar()
        else:
            LoginEntry().start()

        load_cookie(config.cookie_path, jar)
        target_html = conn.get(config.url, cookies=jar)

    soup = BeautifulSoup(target_html.text, 'lxml')
    return soup, conn


def load_cookie(cookie, jar):
    cookies = pickle.load(open(cookie, "rb"))
    for cookie in cookies:
        jar.set(cookie['name'], cookie['value'])


class Entry:
    def __init__(self, config):
        self.config = config
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        if config and config.user_data:
            chrome_options.add_argument('--user-data-dir=' + config.user_data)  # 设置成用户
        if config and config.user_crx:
            chrome_options.add_extension(config.user_crx)  # 自己下载的crx路径'd:\crx\AdBlock_v2.17.crx'
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def start(self):
        try:
            self.perform()
        finally:
            self.driver.close()
