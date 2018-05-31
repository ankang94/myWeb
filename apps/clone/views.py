import json
import os
import pickle
import threading
import uuid

import requests
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from apps.article.models import Article, ArticleGroup, Image, Script
from apps.clone.models import CopyArticle
from clone.base import COOKIE_DIR
from clone.base import Config, create_soup
from myWeb.adapter import Cache
from xadmin.views import BaseAdminView

pic_tmp_path = os.path.join(settings.MEDIA_ROOT, 'tmp')
cookie_dir = os.path.join(COOKIE_DIR, 'csdn.pkl')


class LoginCSDN:
    def perform(self):
        self.driver.get(self.config.url)
        # 显示等待登陆加载
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "login-part")))
        username = '***'
        password = '***'
        js = "$('.login-part:first > h3 > a').click();\
            $('#username').val('" + username + "');\
            $('#password').val('" + password + "');\
            $('#fm1').submit();"
        self.driver.execute_script(js)
        pickle.dump(self.driver.get_cookies(), open(cookie_dir, "wb"), 0)


class CloneArticle(BaseAdminView):
    template_name = 'copy_article.html'

    def get(self, request, *args, **kwargs):
        resp = {'ret': init_clone_template}
        return render(request, self.template_name, resp)

    def post(self, request, *args, **kwargs):
        resp = {'ret': init_clone_template}
        if request.POST.get('save_key'):
            try:
                return save_clone_page(request)
            except Exception as e:
                return HttpResponse(str(e))
        else:
            get_clone_page(request, resp)
        return render(request, self.template_name, resp)


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
                save_img.path.save(save_img.name, File(open(os.path.join(pic_tmp_path, item), 'rb')))
                save_img.save()
                save_article.image.add(save_img)
    if 'code_source' in save_data.keys():
        need_js = Script.objects.get(name='prettify.js')
        need_css = Script.objects.get(name='prettify.css')
        save_article.script.add(need_js, need_css)
    Cache().remove('tops')
    return HttpResponse(save_article.articleid)


def get_clone_page(request, resp):
    host, url, title, h2, h3, context, code, exclude = request.POST.get('host'), \
                                                       request.POST.get('url'), \
                                                       request.POST.get('title'), \
                                                       request.POST.get('h2'), \
                                                       request.POST.get('h3'), \
                                                       request.POST.get('context'), \
                                                       request.POST.get('code'), \
                                                       request.POST.get('exclude')
    config = Config({
        'headers': {'Host': host},
        'url': url,
        'cookie': cookie_dir
    })
    temp_copy_article = {'url': url}
    _soup, _conn = create_soup(config, LoginCSDN)
    # title
    article_title = _soup.select(title)  # 表字段
    if article_title and len(article_title) > 0:
        temp_copy_article['title'] = str(article_title[0].string)
    full_btn = _soup.select("#btn-readmore")
    if full_btn and len(full_btn) > 0:
        full_btn[0].string.replace_with("")
    # context
    article_context = _soup.select("article")
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


def load_img(item, conn, pic_source_list):
    item['class'] = 'img-fluid'
    imgurl = str(item['src'])
    name = str(hash(imgurl))
    pic_source_list.append(name)
    item['alt'] = name
    del item['src']
    with open(os.path.join(pic_tmp_path, name), 'wb') as f:
        f.write(conn.get(imgurl).content)
        f.flush()
        f.close()
