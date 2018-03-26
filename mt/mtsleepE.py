"""
本例中将对 Thread 子类化,而不是直接对其实例化。
这将使我们在定制线程对象时拥有更多的灵活性,也能够简化线程创建的调用过程。

比较 mtsleepD 和 mstsleepE 的代码,其中的几个重要变化:
    1)MyThread子类的构造函数必须先调用其基类的构造函数;
    2)之前的特殊方法__call__()在这个子类中必须要写为 run()。
"""
import threading
from time import sleep, ctime

loops = (4, 2)


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
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
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all DONE at:', ctime())


if __name__ == '__main__':
    main()
