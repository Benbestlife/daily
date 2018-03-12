'''
使用了 thread 模块提供的简单多线程机制。
两个循环是并发执行的(很明显,短的那个先结束),
因此总的运行时间只与最慢的那个线程相关,而不是每个线程运行时间之和。
'''

import _thread
from time import sleep, ctime


def loop0():
    print('start loop 0 at:', ctime())
    sleep(4)
    print('end loop 0 at:', ctime())


def loop1():
    print('start loop 1 at:', ctime())
    sleep(2)
    print('end loop 1 at:', ctime())


def main():
    print('starting at:', ctime())
    # start_new_thread()必须包含开始的两个参数,
    # 于是即使要执行的函数不需要参数,也需要传递一个空元组
    _thread.start_new_thread(loop0, ())
    _thread.start_new_thread(loop1, ())
    sleep(6)
    print('all Done at:', ctime())

'''
sleep(6)调用?
如果没有阻止主线程继续执行, 它将会继续执行下一条语句, 显示“alldone”然后退出,
而loop0()和loop1()这两个线程将直接终止。

这里没有让主线程等待子线程全部完成后再继续的代码,即线程所需的某种形式的同步。
在此例中,调用 sleep()来作为同步机制。
将其值设定为 6 秒是因为我们知道所有线程会在主线程计时到 6 秒之前完成。

是否有比在主线程中额外延时 6 秒更好的线程管理方式?
由于这个延时,整个程序的运行时间并没有比单线程的版本更快。
像这样使用 sleep()来进行线程同步是不可靠的。
如果循环有独立且不同的执行时间要怎么办呢?
我们可能会过早或过晚退出主线程。
这就是引出锁的原因。 参见 mtsleepB.py
'''

if __name__ == '__main__':
    main()