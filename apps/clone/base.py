# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/5/7 上午 9:29'

import json
import os
import pickle
import threading
import uuid

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files import File
from django.utils.safestring import mark_safe
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from apps.article.models import Article, ArticleGroup, Image, Script
from apps.clone.models import CopyArticle
from myWeb.adapter import Cache

COOKIE_DIR = os.path.join(settings.BASE_DIR, 'apps', 'clone', 'cookies')
PIC_TMP_PATH = os.path.join(settings.MEDIA_ROOT, 'tmp')


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


def create_soup(config, *clzz):
    from itertools import chain

    class LoginEntry(*chain(clzz, (Entry,))):
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
                LoginEntry().start()
                jar = RequestsCookieJar()
        else:
            LoginEntry().start()

        load_cookie(config.cookie_path, jar)
        target_html = conn.get(config.url, cookies=jar)

    soup = BeautifulSoup(target_html.text, 'lxml')
    return soup, conn


def load_cookie(cookie, jar):
    if os.path.exists(cookie):
        cookies = pickle.load(open(cookie, "rb"))
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


def init_clone_template():
    template = Cache().get('clone_template')
    if template and len(template) > 0:
        return template
    else:
        template = []
        clone_data = CopyArticle.objects.all()
        for data in clone_data:
            temp = {'name': data.name,
                    'host': data.host,
                    'title': data.title,
                    'context': data.context,
                    }
            if data.h2:
                temp['h2'] = data.h2
            if data.h3:
                temp['h3'] = data.h3
            if data.code:
                temp['code'] = data.code
            if data.exclude:
                temp['exclude'] = data.exclude
            template.append(temp)
            Cache('clone_template', template)
    return json.dumps(template)


def __perform(self):
    pass


def get_clone_page(request, cookie_name, clzz, resp):
    host, url, title, h2, h3, context, code, exclude = request.POST.get('host'), \
                                                       request.POST.get('url'), \
                                                       request.POST.get('title'), \
                                                       request.POST.get('h2'), \
                                                       request.POST.get('h3'), \
                                                       request.POST.get('context'), \
                                                       request.POST.get('code'), \
                                                       request.POST.get('exclude')
    init_config = {'headers': {'Host': host}, 'url': url}
    if cookie_name:
        init_config.update({'cookie': os.path.join(COOKIE_DIR, cookie_name)})
    config = Config(init_config)
    temp_copy_article = {'url': url}
    if not clzz:
        clzz = type('NoEntry', (), {'perform': __perform})
    _soup, _conn = create_soup(config, clzz)
    # title
    article_title = _soup.select(title)  # 表字段
    if article_title and len(article_title) > 0:
        temp_copy_article['title'] = article_title[0].get_text(strip=True)
    # context
    article_context = _soup.select(context)
    if article_context and len(article_context) > 0:
        article = article_context[0]
        # 添加导航
        if h3:
            for item in article.find_all(h3):  # 表字段
                item.name = 'h3'
                item.attrs = []
                item.string = item.get_text(strip=True)
        if h2:
            for item in article.find_all(h2):  # 表字段
                item.name = 'h2'
                item.attrs = []
                item.string = item.get_text(strip=True)
        # 处理代码 -- 这个要处理//简单处理pre代码块
        code_source = article.select(code)
        if len(code_source) > 0:
            temp_copy_article['code_source'] = True
            for item in code_source:
                item['class'] = 'prettyprint'
                item.string = item.get_text()
        # 去除特定元素|分离
        if exclude:
            for exdom in str(exclude).split('|'):
                for item in article.select(exdom):  # ul[class='pre-numbering']
                    item.extract()
        threads = []
        pic_source_list = []
        for item in article.select("img"):
            t = threading.Thread(target=load_img, args=(item, _conn, pic_source_list))
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        temp_copy_article['pic_source'] = pic_source_list
        temp_copy_article['article'] = article.prettify()
    temp_copy_article_id = uuid.uuid1()
    Cache(temp_copy_article_id, temp_copy_article, 60 * 10)
    resp['temp_copy_article_id'] = temp_copy_article_id
    resp['cust_data'] = {'name': request.POST.get('name'),
                         'title': title,
                         'url': url,
                         'h2': h2,
                         'h3': h3,
                         'context': context,
                         'code': code,
                         'exclude': exclude}
    resp['copy_view'] = mark_safe(temp_copy_article['article'])


def save_clone_page(request):
    save_article = Article()
    save_data = Cache().get(request.POST.get('save_key'))
    save_article.group = ArticleGroup.objects.get(groupid=0)
    save_article.title = save_data['title']
    save_article.comment = '转发自网络'
    save_article.summary = '本文转自{0}，侵权删除'.format(save_data['url'])
    save_article.context = save_data['article']
    save_article.save()
    if 'pic_source' in save_data.keys():
        for item in save_data['pic_source']:
            try:
                Image.objects.get(name=str(item))
            except Image.DoesNotExist:
                save_img = Image()
                save_img.name = item
                save_img.path.save(save_img.name, File(open(os.path.join(PIC_TMP_PATH, item), 'rb')))
                save_img.save()
                save_article.image.add(save_img)
    if 'code_source' in save_data.keys():
        need_js = Script.objects.get(name='prettify.js')
        need_css = Script.objects.get(name='prettify.css')
        save_article.script.add(need_js, need_css)
    Cache().remove('tops')
    return save_article.articleid
