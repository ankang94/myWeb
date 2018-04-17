# _*_coding:utf-8_*_
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginZMP:

    def __init__(self, arg):
        self.arg = arg
        self.result = None
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        try:
            # 获取任务单内容
            self.get_task_content(arg)
        except:
            pass
        finally:
            self.driver.close()

    def login_cookie(self):
        username = '***'
        password = '***'
        self.driver.get('https://oa.ztesoft.com')
        # 显示等待登陆加载
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, ".//*[@id='fm_login']/table/tbody/tr[2]/td/table")))
        js = 'document.getElementById(\"edt_username\").value = ' + '\"' + username + '\"' + \
             ';document.getElementById(\"edt_pwd\").value = ' + '\"' + password + \
             '\"' + ';document.getElementById(\"edt_ck\").checked=\"checked\"' + \
             ';document.getElementById(\"login_btn\").click()'
        self.driver.execute_script(js)
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"), 0)

    def get_task_content(self, arg):
        url = 'https://oa.ztesoft.com/queryTransDtl.action?transid=' + \
              arg + '&orgState=O&language=zh_CN'
        if os.path.exists("cookies.pkl"):
            self.driver.get('https://oa.ztesoft.com/Login.jsp')
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        else:
            self.login_cookie()
        self.driver.get(url)
        if 'Login.jsp' in self.driver.current_url:
            # cookie过期重新生成
            self.driver.delete_all_cookies()
            os.remove("cookies.pkl")
            self.login_cookie()
            self.driver.get(url)
        target = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                # (By.XPATH, ".//*[@class='UnderRow'][2]/td[2]/span/table/tbody/tr[12]/td[2]")))
                (By.ID, "recordList")))
        self.result = target.get_attribute('outerHTML')
        # output = open('提交列表.txt', 'w')
        # output.writelines([line +'\n' for line in taskContent.text.split('<br/>')])
        # output.flush()
        # output.close()
        # for x in taskContent.text.split('<br/>'):
        # print(x)
