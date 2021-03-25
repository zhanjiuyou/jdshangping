'''
    此文件为京东cookies获取文件
    用selenium实现，进行登录操作获取cookies
    date:2021.3.3
    author:焦康阳
    blog:http://jiaokangyang.com
'''

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions as ex
import time

class Cookies():
    def __init__(self,username,password):
        # 这里我们使用谷歌浏览器
        self.url = 'https://www.jd.com/'
        self.brower = webdriver.Chrome()
        # 设置最长显示等待时间10s
        self.wait = WebDriverWait(self.brower,30)
        self.username = username
        self.password = password

    # 这里进行模拟登录操作
    def openjd(self):
        self.brower.get(self.url)
        #  打开京东主页，打击登录按钮
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'link-login'))).click()
        # 选择账号密码登录
        self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="login-tab login-tab-r"]/a'))).click()
        # 输入账号
        self.wait.until(EC.presence_of_element_located((By.ID,'loginname'))).send_keys(self.username)
        # 输入密码
        self.wait.until(EC.presence_of_element_located((By.ID,'nloginpwd'))).send_keys(self.password)
        # 点击登录按钮
        self.wait.until(EC.presence_of_element_located((By.ID,'loginsubmit'))).click()

    # 判断账号密码受否错误
    def password_error(self):
        try:
            # 判断是否会出现错误提示，如果出现则出现密码错误提示
            print('正在测试账号密码')
            return bool(self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'msg-error'))))

        except ex.TimeoutException:
            return False

    # 获取cookies
    def getcookies(self):
        return self.brower.get_cookies()

    #  判断账号受否登录成功
    def login_success(self):
        try:
            # 判断页面中是否有退出
            return bool(self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'nickname'))))

        except ex.TimeoutException:
            return False


    def main(self):
        self.openjd()
        # 上面完成打开浏览器填写账号密码操作，验证码这块自己手动操作
        time.sleep(5)
        if self.password_error():
            print('用户名或密码错误')
            self.brower.close()
            return {
                'status':2,
                'content':'用户名或者密码错误'
            }

        elif self.login_success():
            print('登录成功')
            # 获取cookies
            cookies = self.getcookies()

            self.brower.close()
            print(cookies)
            return {
                'status':1,
                'content':cookies
            }

        else:
            print('登录失败')
            self.brower.close()
            return {
                'status':3,
                'content':'登录异常'
            }


