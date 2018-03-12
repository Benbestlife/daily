'''
对 mtsllepE.py 中的 MyThread 类进行修改,
增加一些调试信息的输出,并将其存储,以便在接下来的例子中导入这个类.
除了简单地调用函数外,还将把结果保存在实例属性 self.res 中,
并创建一个新的方法 getResult()来获取这个值。
'''
import threading
from time import sleep, ctime


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        print('开始', self.name, '于:', ctime())
        self.res = self.func(*self.args)
        print(self.name, '结束于:', ctime())
