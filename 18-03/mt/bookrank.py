'''
atexit.register()函数来告知脚本何时结束

它是什么呢?
注册终止函数(即main执行结束后调用的函数)
这个函数(这里使用了装饰器的方式)会在 Python 解释器中注册一个退出函数,
也就是说,它会在脚本退出之前请求调用这个特殊函数。
如果不使用装饰器的方式,也可以直接使用register(_atexit())。

在之前 mtsleepX.py 的例子中,对所有线程使用了 Thread.join()用于阻塞执行,直到每个线程都已退出。
这可以有效阻止主线程在所有子线程都完成之前继续执行,所以输出语句“allDONE at”可以在正确的时间调用。
在这些例子中,对所有线程调用 join()并不是必需的,因为它们不是守护线程。
无论如何主线程都不会在派生线程完成之前退出脚本。
由于这个原因,我们将在 mtsleepF.py中删除所有的 join()操作。
不过,要意识到如果我们在同一个地方显示“all done”这是不正确的。

主线程会在其他线程完成之前显示“all done”,所以我们不能再把 print 调用放在_main()里了。
有两个地方可以放置 print 语句:
1.main()返回之后,
2.或者使用 atexit.register()来注册一个退出函数。
'''

from atexit import register
from threading import Thread
from time import ctime
import requests
from pyquery import PyQuery as pq


class Movie(object):
    def __init__(self):
        self.name = ''
        self.score = 0


def movie_from_div(div):
    e = pq(div)
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    print(m.name, m.score)
    return m


def movies_from_url(url):
    r = requests.get(url)
    page = r.content
    e = pq(page)
    items = e('.item')
    for i in items:
        Thread(target=movie_from_div, args=(i,)).start()


def main():
    url = 'https://movie.douban.com/top250'
    movies_from_url(url)


if __name__ == '__main__':
    main()


@register
def _atexit():
    print('全部完成于：', ctime())
