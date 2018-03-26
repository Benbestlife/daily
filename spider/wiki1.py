from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime

import re
import random

pages = set()
random.seed(datetime.now())


def get_internal_links(bs, include_url):
    """获取页面所有内链的列表"""
    internal_links = []
    # 找出所有以 '/' 开头的链接
    # 注意下面的引号的用法
    model = '^(/|.*' + include_url + ')'

    for link in bs.find_all('a', href=re.compile(model)):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                internal_links.append(link.attrs['href'])

    return internal_links


def get_external_links(bs, exclude_url):
    """获取页面所有外链的列表"""
    external_links = []
    # 找出所有以 'http' 或 'www' 开头且不包含当前 url 的链接
    model = '^(http|www)((?!' + exclude_url + ').)*$'

    for link in bs.find_all('a', href=re.compile(model)):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])

    return external_links


def split_address(address):
    """分解地址"""
    address_parts = address.replace('http://', '').split('/')
    return address_parts


def get_random_external_link(starting_page):
    """获取随机的外部连接"""
    request = Request(starting_page)
    html = urlopen(request)
    bs = BeautifulSoup(html)

    external_links = get_external_links(bs, split_address(starting_page)[0])
    if len(external_links) == 0:
        # TODO 这里没有给位置参数
        internal_links = get_internal_links(bs, starting_page)
        # 随机需要加吗？之前没有仔细看这个的用处...囧
        return get_external_links(bs, internal_links[random.randint(0, len(internal_links) - 1)])
    else:
        return external_links[random.randint(0, len(external_links) - 1)]


def follow_external_only(starting_site):
    """仅限外链"""
    external_link = get_random_external_link(starting_site)
    # 用不用 '+' 有什么区别呢？
    print('随机连接是：', external_link)
    follow_external_only(external_link)


def run():
    follow_external_only('https://www.zhihu.com/')


if __name__ == '__main__':
    run()
