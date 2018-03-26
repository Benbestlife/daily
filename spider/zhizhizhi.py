import os
import requests
from selenium import webdriver
from pyquery import PyQuery

driver = webdriver.PhantomJS()


class Model(object):
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}={}'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n {}>'.format(name, '\n  '.join(properties))
        return s


class RecommendItem(Model):
    def __init__(self):
        self.title = ''
        self.abstract = ''
        self.img = ''


def cached(url):
    folder = 'zhizhizhi'
    filename = url.rsplit('/')[-2] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        if not os.path.exists(path):
            os.mkdir(folder)
        driver.get(url)
        with open(path, 'wb') as f:
            f.write(driver.page_source.encode())
        content = driver.page_source
        return content


def item_from_div(div):
    e = PyQuery(div)
    m = RecommendItem()
    m.title = e('.title_box a').text()
    m.abstract = e('.body_box .text').text()
    m.img = e('.post_box_img img').attr('src')
    return m


def items_from_url(url):
    page = cached(url)
    e = PyQuery(page)
    items = e('.post_box')
    return [item_from_div(i) for i in items]


def download_img(url):
    folder = 'img'
    name = url.split('/')[-1]
    path = os.path.join(folder, name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if os.path.exists(path):
        return
    headers = {
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
    }
    r = requests.get(url, headers)
    with open(path, 'wb') as f:
        f.write(r.content)


def main():
    for i in range(1, 10):
        url = 'https://zhizhizhi.com/d/cn/page/{}/'.format(i)
        items = items_from_url(url)
        [download_img(m.img) for m in items]
        print(items)
    driver.close()


if __name__ == '__main__':
    main()
