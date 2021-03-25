'''
    此文件为最后的总调度文件,主要是实现多个账号多线程下单商品
    整体下单流程：
    1.导入账号密码
    2.生成cookies池，并测试cookies有效性（由于京东cookie有效期只有一天，第二次最好还是重新生成一次cookies）
    3.使用cookies登录到网页，并跳转到我们的指定商品页面，selenium自动点击提前选好的商品属性，然后加入购物车，提交订单，点击结算。
    4.最好我们用多线程执行整个下单流程。

'''
from account import readaccount
from save import RedisClient
from testcookies import CookiesGenerator,TestCookies
from shopping import putong
import threading
from multiprocessing import Process,Pool

'''
    先吧我们要用的常用变量进行设定
'''
# 导入账号的模块开关
account_enabled = False
# 生成cookies和测试模块的开关
cookies_enabled = False
testcookies_enabled = False

# 线程数
thread_number = 2

# 下单的商品链接
shangping_url = 'https://item.jd.com/100014929004.html'
# 要买的商品属性
shuxing = {
    'Y7000京选|超万人好评系列',
    'GTX1650ti|i5/16G/512G/100%sRGB',
}

# 总开关,
class kaiguan():
    # 账号导入模块
    def accountadd(self,enable=account_enabled):
        if enable:
            readaccount(sp='----')

    #cookies生成
    def cookiesadd(self):
        if cookies_enabled:
            CookiesGenerator().run()

    # cookies测试模块
    def testcookies(self):
        if testcookies_enabled:
            TestCookies().run()

    #下单
    def xiadan(self):
        a = putong(shangping_url,shuxing)
        a.run()


    # 下单模块，
    def run(self):
        thread_list = []
        # p = Pool(4)
        # 根据我们设置的数量添加线程
        for i in range(0,thread_number):
            print('启动线程',i)
            # 这块遇到大坑，多线程调用函数只写函数名，千万不要加括号，切记！切记！切记！坑的要死
            a = threading.Thread(target=self.xiadan,args=(),)
            print('加入线程',i)
            thread_list.append(a)
            # thread_list.append(Process(target=putong(url=shangping_url, yanse=shuxing).run(),name=str(i),))


        # 启动线程
        for m in thread_list:
            m.start()

        for thread in thread_list:
            thread.join()


if __name__ == '__main__':
    a = kaiguan()
    a.run()