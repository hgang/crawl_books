from math import ceil

import requests
from bs4 import BeautifulSoup

from config import *
from DBHelper import *


class SubTypeParser:
    sub_type = ''
    type = ''
    page = 1
    total_page = 0;

    def __init__(self, type, sub_type):
        self.type = type
        self.sub_type = sub_type

    def start_parse(self):
        total_number = self.__parse_page_one()
        self.total_page = ceil(total_number / PAGE_NUMBER)
        print("\t总页数:", self.total_page)
        if self.total_page > 1:
            while self.page < self.total_page:
                self.page += 1
                url = self.__get_url(self.page)
                print("正在解析：", url)
                res = requests.get(url)
                res.encoding = 'utf-8'
                bs4 = BeautifulSoup(res.text, 'lxml')
                contents = self.__get_contents(bs4)
                session.add_all(contents)
                # for item in contents:
                #     print(item)

    def __parse_page_one(self):
        url = self.__get_url(self.page)
        print("正在解析：", url)
        res = requests.get(url)
        res.encoding = 'utf-8'
        bs4 = BeautifulSoup(res.text, 'lxml')
        contents = self.__get_contents(bs4)
        session.add_all(contents)
        # self.db.insert_books(self.type, self.sub_type, contents)
        # for item in contents:
        #     print(item['cover_image'])
        pages = bs4.select('.pages')[0].select('span')[-1].text.strip()[1:][:-1]
        print("\t总个数:", pages)
        return int(pages);

    def __get_contents(self, bs4):
        books = bs4.select('.sons')
        for book in books:
            bk = Book(self.type, self.sub_type)
            bk.cover = book.select('a')[0].select('img')[0]['src']
            tmp = book.select('p')[0].select('a')[0]
            bk.title = tmp.text.strip()
            bk.detail_link = tmp['href']
            tmp = book.select('p')[1].text.split('\xa0\xa0')  # 拆分2个空格
            # print(tmp)
            bk.author = tmp[0][3:]
            score_info = tmp[1]
            score = score_info.split('(')[0]
            if len(score) > 0:
                bk.score = float(score)
                bk.score_count = int(score_info.split('(')[1][:-4])
            else:
                bk.score = 0.0
                bk.score_count = 0;
            yield bk
            # print(books)

    def __get_url(self, page):
        return "{0}Default.aspx?p={1}&type={2}".format(URL_GUWEN, page, self.sub_type)