from SubTypeParser import *
from DBHelper import *

from config import *
from multiprocessing.pool import Pool


# 获取顾问的类型（大类型和子类型）
def get_guwen_types():
    res = requests.get(URL_GUWEN)
    res.encoding = 'utf-8'
    bs4 = BeautifulSoup(res.text, 'lxml')
    for classify in bs4.select('.son2'):
        type = classify.select('.sleft')
        if len(type) > 0:
            yield {
                'type': type[0].select('a')[0].text[:-1],
                'sub_types': [item.text for item in classify.select('.sright')[0].select('a')]
            }


# 按照子类型解析每个类型下的古文内容及简介
def get_guwens(type, sub_type):
    subParser = SubTypeParser(type, sub_type)
    subParser.start_parse()


def main():
    # get_guwens('小说家类')
    try:
        types = get_guwen_types();
        for type in types:
            tp = type['type']
            # 将类型写入数据库
            session.add(Type(tp))
            session.add_all([SubType(tp, item) for item in type['sub_types']])
            for item in type['sub_types']:
                # print(item)
                get_guwens(tp, item)
        parse_contents()
    finally:
        session.commit()


# 从数据库读出古文，挨个解析所有古文
def parse_contents():
    books = session.query(Book).all()
    # pool = Pool()
    # pool.map(parse_book, books)
    for book in books:
        parse_book(book)


# 解析古文
def parse_book(bk):
    print('parsing book: ', bk.title, bk.detail_link)
    if bk.finished:
        print(bk.title, ' is already parsed')
        return
    res = requests.get(URL_BASE + bk.detail_link)
    res.encoding = 'utf-8'
    bs4 = BeautifulSoup(res.text, 'lxml')
    intro = bs4.select('.son2')[1]
    author = intro.select('p')[0].text
    intro = intro.text.replace(author, '')
    # 更新简介
    session.query(Book).filter(Book._id == bk._id).update({Book.introduce: intro})
    # print(intro)
    bookconts = bs4.select('.bookcont')
    if len(bookconts) == 1:
        clist = bookconts[0].select('ul')[0].select('a')
        length = len(clist)
        for index in range(length):
            content = Content(bk._id)
            content.position = index
            content.chapter = clist[index].text
            if clist[index].has_attr('href'):
                content.detail_link = clist[index]['href']
                get_chapter_detail(content)
            else:
                session.add(content)
    elif len(bookconts) > 1:
        index = 0
        for item in bookconts:
            for it in item.select('a'):
                content = Content(bk._id)
                content.season = item.select('.bookMl')[0].text
                content.position = index
                content.chapter = it.text
                if it.has_attr('href'):
                    content.detail_link = it['href']
                    get_chapter_detail(content)
                else:
                    session.add(content)
                index += 1
    session.query(Book).filter(Book._id == bk._id).update({Book.finished: True})
    session.commit()
    print(bk.title, ' has parse finished')


# 解析文章的详情
def get_chapter_detail(content):
    if len(session.query(Content).filter(Content.detail_link == content.detail_link).all()) > 0:
        print(content.chapter, ' is already exist')
        return;
    try:
        res = requests.get(URL_BASE + content.detail_link)
        res.encoding = 'utf-8'
        bs4 = BeautifulSoup(res.text, 'lxml')
        sections = bs4.select('.bookvson2')[0].select('p')[1:]
        data = ''
        length = len(sections)
        for index in range(length):
            data += sections[index].text
            if index < length - 1:
                data += '\n'
        content.data = data;
        tmp = bs4.select('.son5')
        if len(tmp) > 0:
            interpret_id = bs4.select('.son5')[0]['id'].replace('bfanyiShort', '')
            content.interpret = get_chapter_interpret(interpret_id)
        if len(tmp) > 1:
            analyze_id = bs4.select('.son5')[1]['id'].replace('bshangxiShort', '')
            content.analyze = get_chapter_analyze(analyze_id)
    except Exception as e:
        print(e)
    finally:
        session.add(content)


# 解析文章的翻译
def get_chapter_interpret(id):
    url = 'http://so.gushiwen.org/guwen/ajaxbfanyi.aspx?id=' + id
    res = requests.get(url)
    res.encoding = 'utf-8'
    bs4 = BeautifulSoup(res.text, 'lxml')
    data = bs4.text.strip().split('\n')[2:]
    ret = ''
    for item in data:
        if len(item.strip()) == 0:
            continue;
        ret = ret + item.strip() + '\n'
    return ret


# 解析文章的赏析
def get_chapter_analyze(id):
    url = 'http://so.gushiwen.org/guwen/ajaxbshangxi.aspx?id=' + id
    res = requests.get(url)
    res.encoding = 'utf-8'
    bs4 = BeautifulSoup(res.text, 'lxml')
    data = bs4.text.strip().split('\n')[2:]
    ret = ''
    for item in data:
        if len(item.strip()) == 0:
            continue;
        ret = ret + item.strip() + '\n'
    return ret


def test():
    res = requests.get(URL_BASE + '/guwen/bookv_25.aspx')
    res.encoding = 'utf-8'
    bs4 = BeautifulSoup(res.text, 'lxml')
    sections = bs4.select('.bookvson2')[0].select('p')[1:]
    data = ''
    length = len(sections)
    for index in range(length):
        data = data + sections[index].text
        if index < length - 1:
            data = data + '\n'
    print(data)
    # id = bs4.select('.son5')[0]['id'].replace('bfanyiShort', '')
    # print(id)


if __name__ == '__main__':
    parse_contents()
    # main()
    # test()
    # get_chapter_interpret('758')
    # get_chapter_analyze('1882')
