from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime

import random
import re

random.seed(datetime.now())
pages = set()


def get_links(url):
    global pages
    request = Request('http://en.wikipedia.org' + url)
    html = urlopen(request)
    bs = BeautifulSoup(html)
    # 获取标题、第一段内容、及编辑连接
    # 这里 try 语句有问题，需要修复
    try:
        h1 = bs.h1.get_text()
        print('h1:', h1)
        content1 = bs.find(id='mw-content-text').find_all('p')[0]
        print('content1:', content1)
        edit = bs.find(id='ca-edit').find('span').find('a').attrs['href']
        print('edit:', edit)
    except AttributeError:
        print('页面缺少属性')
    # 获取 wiki 内链
    for link in bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # 新页面
                newpage = link.attrs['href']
                print('newpage:----------------------------', newpage)
                pages.add(newpage)
                # 如果递归运行的次数非常多,前面的递归程序就很可能崩溃。
                # 默认的递归限制是 1000 次
                get_links(newpage)
    return pages


def run():
    links = get_links('/wiki/Kevin_Bacon')
    while len(links) > 0:
        newaticle = links[random.randint(0, len(links) - 1)].attrs['href']
        print('new:', newaticle)
        # 书中这样写，但总觉有问题
        # 下面的links是否覆盖了上面的links，是否影响循环?
        links = get_links(newaticle)
        print(links)


if __name__ == '__main__':
    run()
