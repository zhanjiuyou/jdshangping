'''
    说明：此文件为京东购买商品程序
    date:2021.3.6
    author:焦康阳
    blog:https://jiaokangyang.com
'''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from save import RedisClient
from datetime import datetime
from selenium.webdriver.common.by import By
import selenium.common.exceptions as ex
import json
import time

# 普通商品购买流程，这里由于有的商品有多个属性，所以我们yanse使用字典
class putong():
    def __init__(self,url,yanse):
        self.url = url
        # yanse为为我们下单上面的颜色类目选项
        self.yanse = yanse
        self.brower = webdriver.Chrome()
        self.wait = WebDriverWait(self.brower,30)
        self.cookies_db = RedisClient('jdcookies')

    #先进行登录
    def login(self):
        print(datetime.now().strftime('%Y-%m-%d  %H:%M:%S '),'开始使用cookies登录账号')
        #随机获取一个账号的cookies
        if self.cookies_db.count() != 0:
            username,cookie = self.cookies_db.random_getall()
            cookies = json.loads(cookie)
            print(datetime.now().strftime('%Y-%m-%d  %H:%M:%S '),'成功获取到账号%s的cookies'%username)
        else:
            print('没有可用的cookies，请重新获取后再进行登录')
            return False

        self.brower.get('https://www.jd.com/')
        for cookie in cookies:
            self.brower.add_cookie(cookie)

        self.brower.get(self.url)

        try:
            # 判断账号是否登录成功
            return bool(self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'nickname')))),username

        except ex.TimeoutException:
            return False

    # 选择商品加入购物车
    def choice(self):
        try:
            # 遍历yanse中设定的值，也就是我们要选择的商品属性,有的商品有多个属性同时选择，所以我们要添加多个
            for i in self.yanse:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"正在选择属性",i)
                self.wait.until(EC.presence_of_element_located((By.LINK_TEXT,i)))

            #选择属性后点击加入购物车
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="choose-btns"]/a[@id="InitCartUrl"]'))).click()
            # 商品加入成功后京东会自动跳入到成功页面，我们检测整个CSS就行
            if self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'success-lcol'))):
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'商品已成功加入购物车')
                return True
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'商品加入购物车失败')
                return False
        except ex.TimeoutException:
            return False

    # 购物车页面进行结算
    def pay(self):
        try:
            # 打开购物车页面
            self.brower.get('https://cart.jd.com/cart_index/')
            # 点击全选。这块跳转到结算界面京东自动打勾了，这里我们不用自己操作
            # self.wait.until(EC.presence_of_element_located((By.NAME,'select-all'))).click()
            time.sleep(2)
            # 点击结算
            self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, '去结算'))).click()
            time.sleep(2)

            self.wait.until(EC.presence_of_element_located((By.ID, 'order-submit'))).click()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "已提交订单")
            return True
        except ex.TimeoutException:
            print('页面超时')
            return False

    #进行登录下单流程
    def run(self):
        a,username = self.login()
        if a:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "账号%s登录成功"%username)
            # 登录成功后选择商品属性
            if self.choice():
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "商品属性选择完毕并成功加入购物车")
                if self.pay():
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "账号%s的用户已成功提交订单，请及时支付"%username)
                    self.brower.close()
                else:
                    print('订单提交失败')
                    self.brower.close()
            else:
                print('商品选择失败')
                self.brower.close()

# a = putong('https://item.jd.com/100014929004.html',{
#     'Y7000京选|超万人好评系列',
#     'GTX1650ti|i5/16G/512G/100%sRGB',
# })
# a.run()