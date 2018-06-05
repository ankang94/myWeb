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
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

COOKIE_DIR = os.path.join(settings.BASE_DIR, 'apps', 'clone', 'cookies')
PIC_TMP_PATH = os.path.join(settings.MEDIA_ROOT, 'tmp')


class Config:
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


class BaseEntry:
    signal, username, password, script, cookie_dir = (None,) * 5

    def perform(self):
        self.driver.get(self.config.url)
        # 显示等待登陆加载
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.CLASS_NAME, self.signal)))
        js = self.script.format(self.username, self.password)
        self.driver.execute_script(js)
        pickle.dump(self.driver.get_cookies(), open(self.cookie_dir, "wb"), 0)


def create_soup(config, *clzz):
    from itertools import chain
    if len(clzz) == 0 or not clzz[0]:
        def __perform(self):
            pass

        clzz = (type('NoEntry', (), {'perform': __perform}),)

    class WebEntry(*chain(clzz, (Entry,))):

        def __init__(self):
            super(clzz[-1], self).__init__(config)

    conn = requests.session()
    conn.headers = config.headers
    conn.verify = False
    target_html = conn.get(config.url)
    if config.url != target_html.url and config.cookie_path:
        jar = RequestsCookieJar()
        if os.path.exists(config.cookie_path):
            load_cookie(config.cookie_path, jar)
            # 添加session再次访问
            target_html = conn.get(config.url, cookies=jar)
            # 重定向重新获取session
            if config.url != target_html.url:
                WebEntry().start()
                jar = RequestsCookieJar()
        else:
            WebEntry().start()

        load_cookie(config.cookie_path, jar)
        target_html = conn.get(config.url, cookies=jar)

    soup = BeautifulSoup(target_html.text, 'lxml')
    return soup, conn


def load_cookie(cookie_path, jar):
    if os.path.exists(cookie_path):
        cookies = pickle.load(open(cookie_path, "rb"))
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])


def load_img(item, conn, pic_source_list):
    item['class'] = 'img-fluid'
    imgurl = str(item['src'])
    name = str(hash(imgurl))
    pic_source_list.append(name)
    item['alt'] = name
    del item['src']
    with open(os.path.join(PIC_TMP_PATH, name), 'wb') as f:
        f.write(conn.get(imgurl).content)
        f.flush()
        f.close()
