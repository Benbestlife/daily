'''
本例比较了递归求斐波那契、阶乘与累加函数的执行。
该脚本按照单线程的方式运行这三个函数。
之后使用多线程的方式执行同样的任务,用来说明多线程环境的优点。

以单线程模式运行时,只是简单地依次调用每个函数,并在函数执行结束后立即显示相应的结果。
而以多线程模式运行时,并不会立即显示结果。
因为我们希望让 MyThread 类越通用越好(有输出和没有输出的调用都能够执行),
我们要一直等到所有线程都执行结束,然后调用getResult()方法来最终显示每个函数的返回值。
'''
from time import sleep, ctime

from mt.myThread import MyThread


def fib(x):
    sleep(0.005)
    if x < 2:
        return 1
    return fib(x - 2) + fib(x - 1)


def fac(x):
    sleep(0.1)
    if x < 2:
        return 1
    return x * fac(x - 1)


def sum(x):
    sleep(0.1)
    if x < 2:
        return 1
    return x + sum(x - 1)

funcs = [fib, fac, sum]
n = 12


def main():
    nfuncs = range(len(funcs))

    print('*** 单线程')
    for i in nfuncs:
        print('开始', funcs[i].__name__, '于:', ctime())
        print(funcs[i](n))
        print(funcs[i].__name__, '结束于:', ctime())

    print('*** 多线程')
    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (n,), funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()
        print(threads[i].getResult())

    print('结束')

if __name__ == '__main__':
    main()