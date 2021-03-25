'''
    此文件为账号导入模块，将我们提前写好的账号全部导入到redis中
    我们单独建立一个account.txt来集中存放账号密码，来提高效率
    date:2021.3.2
    author:焦康阳
    blog：https://jiaokangyang.com
'''

from save import RedisClient

jd = RedisClient('jdaccount')
# 我们txt文件中用----将账号密码隔开，
def readaccount(sp='----'):
    print('开始导入账号密码,正在读取account.txt')
    with open('account.txt','r') as f:
        datas = f.readlines()
        for data in datas:
            username,password = data.strip('\n').split(sp)
            print('正在导入账号：%s 密码：%s'%(username,password))
            result = jd.set(username,password)
            print('导入成功' if result else '导入失败')


