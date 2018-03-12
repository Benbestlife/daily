'''
mtsleepF.py 应用派生了随机数量的线程,
当每个线程执行结束时它会进行输出。

这里有一个新功能,使用集合来记录剩下的还在运行的线程。
我们对集合进行了子类化而不是直接使用,这是因为我们想要演示另一个用例:变更集合的默认可印字符串。

当显示一个集合时,你会得到类似 set([X, Y, Z,...])这样的输出。
而应用的用户并不需要(也不应该)知道关于集合的信息或者我们使用了这些集合。
我们只需要显示成类似 X,Y,Z, ...这样即可。
这也就是派生了 set 类并实现了它的__str__()方法的原因。

如果不幸,
1.一个问题是输出可能部分混乱(因为多个线程可能并行执行I/O)
之前的几个示例代码也都有交错输出的问题存在。
2.另一问题则出现在两个线程修改同一个变量(剩余线程名集合)时.

I/O 和访问相同的数据结构都属于临界区,因此需要用锁来防止多个线程同时进入临界区。
为了加锁,需要添加一行代码来引入 Lock(或 RLock),然后创建一个锁对象,
因此需要添加/修改代码以便在合适的位置上包含这些行。

作为维护你自己的当前运行线程集合的一种替代方案,可以考虑使用threading.enumerate(),
该方法会返回仍在运行的线程列表(包括守护线程,但不包括没有启动的线程)。
在本例中并没有使用这个方案,因为它会显示两个额外的线程,所以我们需要删除这两个线程以保持输出的简洁。
这两个线程是当前线程(因为它还没结束),以及主线程(没有必要去显示)。

如果只需要对当前运行的线程进行计数,那么可以使用 threading.active_count()来代替
'''

from atexit import register
from random import randrange
from threading import Thread, current_thread, Lock
from time import ctime, sleep


class CleanOutputSet(set):
    def __str__(self):
        return ', '.join(x for x in self)


lock = Lock()  # 创建锁对象
loops = (randrange(2, 5) for x in range(randrange(3, 7)))
# 以下的替代方案　threading.enumerate()
remaining = CleanOutputSet()


def loop(nsec):
    '''
    使用 with 语句,此时每个对象的上下文管理器负责在进入该套件之前调用 acquire(),
    并在完成执行之后调用 release().
    with lock:
        remaining.add(myname)
        print('xxx')
    sleep(nsec)
    '''
    myname = current_thread().name
    # 指明启动线程的输出操作是原子的(没有其他线程可以进入临界区)
    lock.acquire()  # 获得一个锁
    remaining.add(myname)
    print('{} 已经开始 {}'.format(ctime(), myname))
    lock.release()  # 释放一个锁
    sleep(nsec)
    lock.acquire()
    remaining.remove(myname)
    print('{} 已经完成 {} ({} secs)'.format(ctime(), myname, nsec))
    print('    (remaining: {})'.format(remaining or 'NONE'))
    lock.release()


def main():
    for pause in loops:
        Thread(target=loop, args=(pause,)).start()


@register
def _atexit():
    print('所有完成于：', ctime())


if __name__ == '__main__':
    main()
