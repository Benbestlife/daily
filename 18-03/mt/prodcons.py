"""
本例演示了生产者-消费者模型这个场景。

在这个场景下,商品或服务的生产者生产商品,然后将其放到类似队列的数据结构中。
生产商品的时间是不确定的,同样消费者消费生产者生产的商品的时间也是不确定的。
简单而言,就是创建一个队列,让生产者(线程)在其中放入新的商品,而消费者(线程)消费这些商品。

该生产者-消费者问题的实现使用了 Queue 对象,以及随机生产(消费)的商品的数量。
生产者和消费者独立且并发地执行线程.

对于一个要执行多个任务的程序,可以让每个任务使用单独的线程。
相比于使用单线程程序完成所有任务,这种程序设计方式更加整洁。
"""

from random import randint
from time import sleep
from queue import Queue
from myThread import MyThread


def writeq(queue):
    print('为队列生产对象...')
    queue.put('xxx', 1)
    print('现在，队列的大小为：', queue.qsize())


def readq(queue):
    queue.get(1)
    print('从队列中消费对象...现在，队列的大小为：', queue.qsize())


def writer(queue, loops):
    for i in range(loops):
        writeq(queue)
        sleep(randint(1, 3))


def reader(queue, loops):
    for i in range(loops):
        writeq(queue)
        sleep(randint(2, 5))


funcs = [writer, reader]
nfuncs = range(len(funcs))


def main():
    nloops = randint(2, 5)
    q = Queue(32)

    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print('全部完成')


if __name__ == '__main__':
    main()
