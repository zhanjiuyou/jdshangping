'''
    此文件为为生成cookies，并测试cookies
    date:2021.3.4
    author:焦康阳
    blog:https://jiaokangyang.com

'''

from save import RedisClient
from cookies import Cookies
import json
import time
import requests

# 此类为获取cookies
class CookiesGenerator():
    def __init__(self,name='jdcookies'):
        self.name = name
        self.account_db = RedisClient('jdaccount')
        self.cookies_db = RedisClient(self.name)

    def process_cookies(self,cookies):
        dict = {}
        # 提取cookies中的name和value组成新字典
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']

        return dict

    def run(self):
        # 提取redis数据库中的账号，进行对比，看哪个账号换没有获取cookies
        account_usernames = self.account_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        for username in account_usernames:
            # 如果账号没有存在与cookies表中说明没有获取cookies
            if not username in cookies_usernames:
                password = self.account_db.get(username)
                print('正在生成账号为%s的cookies'%username)
                # 这块是我们cookies文件中的返回结果
                result = Cookies(username,password).main()
                time.sleep(10)
                if result.get('status') == 1:
                    # cookies = self.process_cookies(result.get('content'))
                    cookies = result.get('content')
                    print('成功获取到cookies',cookies)
                    if self.cookies_db.set(username,json.dumps(cookies)):
                        print("成功保存cookies")

                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.account_db.delete(username):
                        print('成功删除错误账号')

                else:
                    print(result.get('content'))


# 此类为测试cookies模块
class TestCookies():
    def __init__(self):
        self.account_db = RedisClient('jdaccount')
        self.cookies_db = RedisClient('jdcookies')
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
        }
        self.testUrl = 'https://www.jd.com/'

    def test(self,username,cookies):
        print('开始测试账号为%s的cookies'%username)
        try:
            # 测试格式是否为json格式
            json.dumps(cookies)
        except TypeError:

            print('cookies不合法',username)
            self.cookies_db.delete(username)
            print('删除cookies',username)
            return

        try:
            # 加入cookies测试有效性
            response = requests.get(self.testUrl,headers=self.headers,cookies=cookies,timeout=5,allow_redirects=False)
            if response.status_code == 200:
                print('账号%s的cookies有效'%username)
            else:
                print(response.status_code,response.headers)
                print('账号%s的cookies已失效'%username)
                self.cookies_db.delete(username)
                print('删除cookies',username)
        except ConnectionError as e:
            print('发生异常',e.args)

    def process_cookies(self,cookies):
        dict = {}
        # 提取cookies中的name和value组成新字典，可供requests调用的cookies
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']

        return dict


    def run(self):
        # 获取cookies表中的所有账号cookies
        cookies_groups = self.cookies_db.all()
        for username,cookies in cookies_groups.items():
            # 将JSON格式转换为字典
            a = json.loads(cookies)
            # 将selenium生成的cookies转换为requests需要的格式进行测试
            b = self.process_cookies(a)

            self.test(username,b)
# a = CookiesGenerator()
# a = TestCookies()
# a.run()