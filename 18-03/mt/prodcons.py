'''
本例演示了生产者-消费者模型这个场景。
在这个场景下,商品或服务的生产者生产商品,然后将其放到类似队列的数据结构中。
生产商品的时间是不确定的,同样消费者消费生产者生产的商品的时间也是不确定的。

简单而言,就是创建一个队列,让生产者(线程)在其中放入新的商品,而消费者(线程)消费这些商品。

该生产者-消费者问题的实现使用了 Queue 对象,以及随机生产(消费)的商品的数量。
生产者和消费者独立且并发地执行线程.
'''
from random import randint
from time import sleep
from queue import Queue
from myThread import MyThread


def writeQ(queue):
    print('')


def readQ(queue):
    pass


def writer(queue, loops):
    pass


def reader(queue, loops):
    pass


def main():
    pass


if __name__ == '__main__':
    main()
