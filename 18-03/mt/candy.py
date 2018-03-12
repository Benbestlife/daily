'''
在这个例子中,我们将使用锁和信号量来模拟一个简化的糖果机。
这个特制的机器只有 5 个可用的槽来保持库存(糖果)。
如果所有的槽都满了,糖果就不能再加到这个机器中了;
相似地,如果每个槽都空了,想要购买的消费者就无法买到糖果了。
我们可以使用信号量来跟踪这些有限的资源(糖果槽)。

threading 模块包括两种信号量类:Semaphore 和 BoundedSemaphore。
信号量实际上就是计数器,它们从固定数量的有限资源起始。

当分配一个单位的资源时,计数器值减 1,而当一个单位的资源返回资源池时,计数器值加 1。
BoundedSemaphore 的一个额外功能是这个计数器的值永远不会超过它的初始值,
换句话说,它可以防范其中信号量释放次数多于获得次数的异常用例。


'''
from atexit import register
from random import randrange
from threading import (
    BoundedSemaphore,
    Lock,
    Thread,
)
from time import sleep, ctime

lock = Lock()
MAX = 5
candytray = BoundedSemaphore(MAX)


# 这段代码是一个临界区, 这就是为什么获取锁是执行所有行的仅有方法。
def refill():
    lock.acquire()
    print('重新填装糖果...')
    try:
        candytray.release()
    except ValueError:
        print('满的，跳过')
    else:
        print('OK')
    lock.release()


'''
buy()是和 refill()相反的函数,它允许消费者获取一个单位的库存。
条件语句检测是否所有资源都已经消费完。
计数器的值不能小于 0,因此这个调用一般会在计数器再次增加之前被阻塞。
通过传入非阻塞的标志 False,让调用不再阻塞,而在应当阻塞的时候返回一个 False,指明没有更多的资源了
'''


def buy():
    lock.acquire()
    print('购买糖果...')
    if candytray.acquire(False):
        print('OK')
    else:
        print('空的，跳过')
    lock.release()


def producer(loops):
    for i in range(loops):
        refill()
        sleep(randrange(3))


def consumer(loops):
    for i in range(loops):
        buy()
        sleep(randrange(3))


def main():
    print('开始于：', ctime())
    nloops = randrange(2, 6)
    print('糖果机器共有 {} 糖果'.format(MAX))
    Thread(target=consumer, args=(randrange(nloops, nloops + MAX + 2),)).start()
    Thread(target=producer, args=(nloops,)).start()


'''
创建消费者/买家的线程时进行了额外的数学操作,用于随机给出正偏差,
使得消费者真正消费的糖果数可能会比供应商/生产者放入机器的更多
(否则,代码将永远不会进入消费者尝试从空机器购买糖果的情况)。
'''


@register
def _atexit():
    print('全部结束于：', ctime())


if __name__ == '__main__':
    main()
