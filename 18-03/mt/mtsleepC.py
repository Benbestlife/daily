'''
与使用 thread 模块相比做了哪些修改?
    使用thread时实现的锁没有了,取而代之的是一组 Thread 对象。
    实例化每个 Thread 对象时,把函数(target)和参数(args)传进去,然后得到返回的 Thread 实例。

    Thread()
        实例化Thread(调用Thread())和调用thread.start_new_thread()的最大区别是新线程不会立即开始执行。
        这是一个非常有用的同步功能,尤其是当你并不希望线程立即开始执行时。
    start()
        当所有线程都分配完成之后,通过调用每个线程的 start()方法让它们开始执行,而不是在这之前就会执行。
    join()
        相比于管理一组锁(分配、获取、释放、检查锁状态等)而言,这里只需要为每个线程调用 join()方法即可。
        join()方法将等待线程结束,或者在提供了超时时间的情况下,达到超时时间。
        使用 join()方法要比等待锁释放的无限循环更加清晰(这也是这种锁又称为自旋锁的原因)。
        对于 join()方法而言,其另一个重要方面是它根本不需要调用。
        一旦线程启动,它们就会一直执行,直到给定的函数完成后退出。
        如果主线程还有其他事情要去做,而不是等待这些线程完成(例如其他处理或者等待新的客户端请求),
        就可以不调用 join()。
        join()方法只有在你需要等待线程完成的时候才是有用的。
'''

import threading
from time import sleep, ctime

loops = [4, 2]


def loop(nloop, nsec):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())


def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(
            target=loop,
            args=(i, loops[i]),
        )
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all DONE at:', ctime())


if __name__ == '__main__':
    main()
