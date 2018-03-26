"""待修改"""
import os
import requests
from pyquery import PyQuery as pq


class Model():
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    def __init__(self):
        self.pic_url = ''
        self.p_url = ''


def cached_url(url):
    folder = 'cached'
    filename = url.split('/')[-1]
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
    return r.content


def movie_from_div(div):
    e = pq(div)
    m = Movie()
    m.pic_url = e('a').attr('href')
    return m


def movies_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('.gallary_wrap td')
    movies = [movie_from_div(i) for i in items]
    return movies


def c_url(url):
    folder = '图片地址'
    filename = url.split('/')[-1]
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
    return r.content


def m_from_div(div):
    e = pq(div)
    m = Movie()
    m.p_url = e('img').attr('src')
    return m


def ms_from_url(url):
    page = c_url(url)
    e = pq(page)
    items = e('.gallary_item td')
    movies = [m_from_div(i) for i in items]
    return movies


def download_image(url):
    folder = "美图"
    name = url.split("/")[-1]
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


def page_all(home):
    ms = movies_from_url(home)
    for i in range(2, 50):
        url = 'http://www.xiumeim.com/albums/page-{}.html'.format(i)
        ms = movies_from_url(url)
    print('pic_url:', [m.pic_url for m in ms])
    return [m.pic_url for m in ms]


def page_one(url):
    ms = ms_from_url(url)
    print('ms', ms)
    [download_image(m.p_url) for m in ms]
    for i in range(2, 10):
        uz = url.split('.html')[-2]
        u = uz + '-{}'.format(i) + '.html'
        print('u', u)
        movies = ms_from_url(u)
        [download_image(m.p_url) for m in movies]

def main():
    home = "http://www.xiumeim.com/albums/index.html"
    ps = page_all(home)
    for p in ps:
        page_one(p)


if __name__ == '__main__':
    main()
