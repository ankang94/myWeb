import os
import pickle

from django.http import HttpResponse
from django.shortcuts import render
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from clone.base import COOKIE_DIR, init_clone_template, save_clone_page, get_clone_page
from xadmin.views import BaseAdminView


class LoginCSDN:
    cookie_dir = os.path.join(COOKIE_DIR, 'csdn.pkl')

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
        pickle.dump(self.driver.get_cookies(), open(self.cookie_dir, "wb"), 0)


########################################################################################################################
# 爬虫匹配
reptilian = {
    'blog.csdn.net': {'name': 'csdn.pkl', 'clazz': LoginCSDN},
    'blog.51cto.com': {}
}
########################################################################################################################


# 'csdn.pkl'
class CloneArticle(BaseAdminView):
    template_name = 'copy_article.html'

    def get(self, request, *args, **kwargs):
        resp = {'ret': init_clone_template}
        return render(request, self.template_name, resp)

    def post(self, request, *args, **kwargs):
        resp = {'ret': init_clone_template}
        if request.POST.get('save_key'):
            try:
                return HttpResponse(save_clone_page(request))
            except Exception as e:
                return HttpResponse(str(e))
        else:
            try:
                pool = reptilian.get(request.POST.get('host'))
                get_clone_page(request, pool.get('name'), pool.get('clazz'), resp)
            except Exception as e:
                resp['error'] = str(e)
        return render(request, self.template_name, resp)
