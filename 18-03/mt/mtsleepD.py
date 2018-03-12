'''
本例中,将传递进去一个可调用类(实例)而不仅仅是一个函数。
相比于 mtsleepC.py,这个实现中提供了更加面向对象的方法。

添加了ThreadFunc类,并在实例化 Thread 对象时,同时实例化了可调用类 ThreadFunc。
实际上,这里完成了两个实例化。
为了ThreadFunc类更加通用,而不是局限于 loop()函数,因此添加了一些新的东西,
比如让这个类保存了函数的参数、函数自身以及函数名的字符串。
而构造函数__init__()用于设定上述这些值。
当创建新线程时,Thread 类的代码将调用 ThreadFunc 对象,此时会调用__call__()这个特殊方法。
由于已经有了要用到的参数,这里就不需要再将其传递给 Thread()的构造函数了,直接调用即可。
'''

import threading
from time import sleep, ctime

loops = [4, 2]


class ThreadFunc(object):
    def __init__(self, func, args, name=''):
        self.name = name
        self.func = func
        self.args = args

    def __call__(self):
        self.func(*self.args)


def loop(nloop, nsec):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())


def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=ThreadFunc(loop, (i, loops[i]), loop.__name__))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all DONE at:', ctime())


if __name__ == '__main__':
    main()
