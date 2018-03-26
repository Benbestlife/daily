"""
修改 mtsleepA.py 代码,引入锁,并去除单独的循环函数.
通过使用锁,可以在所有线程全部完成执行后立即退出。
与 mtsleepA.py 中调用 sleep()来挂起主线程不同,锁的使用将更加合理。
"""

import _thread
from time import sleep, ctime


# 不再把 4 秒和 2 秒硬编码到不同的函数中,
# 而是使用了唯一的 loop()函数,并把这些常量放进列表loops 中。
loops = [4, 2]


def loop(nloop, nsec, lock):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())
    # 释放对应的锁,向主线程表明该线程已完成
    lock.release()


def main():
    """
    第一个循环
    上锁
    通过使用 thread.allocate_lock()函数得到锁对象
    通过 acquire()方法取得每个锁, 取得锁--效果相当于“把锁锁上”
    一旦锁被锁上后,就可以把它添加到锁列表 locks 中

    第二个循环用于派生线程,每个线程会调用 loop()函数,
    并传递循环号、睡眠时间以及用于该线程的锁这几个参数。
    为什么不在上锁的循环中启动线程?
    两个原因:
    其一,想要同步线程,以便“所有的马同时冲出围栏”;
    其二,获取锁需要花费一点时间。如果线程执行得太快,有可能出现获取锁之前线程就执行结束的情况。

    第三个循环
    每个线程执行完成后,它会释放自己的锁对象。
    最后一个循环只是坐在那里等待(暂停主线程),直到所有锁都被释放之后才会继续执行。
    因为是按照顺序检查每个锁,所以可能会被排在循环列表前面但是执行较慢的循环所拖累。
    这种情况下,大部分时间是在等待最前面的循环。
    当这种线程的锁被释放时,剩下的锁可能早已被释放(也就是说,对应的线程已经执行完毕)。
    结果就是主线程会飞快地、没有停顿地完成对剩下锁的检查。
    """
    print('starting at:', ctime())
    # 创建一个锁的列表
    locks = []
    nloops = range(len(loops))

    for i in nloops:
        lock = _thread.allocate_lock()
        lock.acquire()
        locks.append(lock)

    for i in nloops:
        _thread.start_new_thread(loop, (i, loops[i], locks[i]))

    for i in nloops:
        while locks[i].locked():
            pass
    print('all DONE at:', ctime())


if __name__ == '__main__':
    main()
