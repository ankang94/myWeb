import re
from django.shortcuts import render
from clone.base import Config, create_soup
from myWeb.adapter import Cache


# def test_index(request):
#     import pickle
#     import os
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support.ui import WebDriverWait
#     from selenium.webdriver.support import expected_conditions as EC
#     from clone.base import COOKIE_DIR
#     ret = {}
#     cookie_dir = os.path.join(COOKIE_DIR, 'zmp.pkl')
#
#     class LoginZMP:
#         def perform(self):
#             url = 'https://oa.ztesoft.com/queryTransDtl.action?transid=' + \
#                   str(self.args) + '&orgState=O&language=zh_CN'
#             if os.path.exists(cookie_dir):
#                 self.driver.get('https://oa.ztesoft.com/Login.jsp')
#                 cookies = pickle.load(open(cookie_dir, "rb"))
#                 for cookie in cookies:
#                     self.driver.add_cookie(cookie)
#             else:
#                 self.login_cookie()
#             self.driver.get(url)
#             if 'Login.jsp' in self.driver.current_url:
#                 # cookie过期重新生成
#                 self.driver.delete_all_cookies()
#                 os.remove(cookie_dir)
#                 self.login_cookie()
#                 self.driver.get(url)
#
#         def login_cookie(self):
#             username = '***'
#             password = '***'
#             self.driver.get('https://oa.ztesoft.com')
#             # 显示等待登陆加载
#             WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
#                 (By.XPATH, ".//*[@id='fm_login']/table/tbody/tr[2]/td/table")))
#             js = 'document.getElementById(\"edt_username\").value = ' + '\"' + username + '\"' + \
#                  ';document.getElementById(\"edt_pwd\").value = ' + '\"' + password + \
#                  '\"' + ';document.getElementById(\"edt_ck\").checked=\"checked\"' + \
#                  ';document.getElementById(\"login_btn\").click()'
#             self.driver.execute_script(js)
#             pickle.dump(self.driver.get_cookies(), open(cookie_dir, "wb"), 0)
#
#     if request.POST and request.POST['taskId']:
#         task_id = request.POST['taskId']
#         if not Cache().get(task_id):
#             config = Config({'args': task_id})
#             soup = create_soup(True, config, LoginZMP)
#
#             def filter_tag_with_parent(tag):
#                 return tag.name == 'td' and re.match('(U|A)\s{3}branches', tag.text)
#
#             uptext = soup.find(filter_tag_with_parent)
#             task_list = [str(x) for x in uptext.get_text('\n', 'br/').split('\n')] if uptext else None
#             if task_id and len(task_id) > 0:
#                 Cache(task_id, task_list, 60 * 15)
#             ret['list'] = task_list
#         else:
#             ret['list'] = Cache().get(task_id)
#     return render(request, 'copy_article.html', ret)


def clone_web_article(request):
    pass