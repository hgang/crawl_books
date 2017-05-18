from SubTypeParser import *
from bak.DBHelper_bak import *

from config import *


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


def get_guwens(type, sub_type, db):
    subParser = SubTypeParser(type, sub_type, db)
    subParser.start_parse()


def main():
    # get_guwens('小说家类')
    db = DBHelper()
    if db:
        try:
            types = get_guwen_types();
            for type in types:
                tp = type['type']
                db.insert_types(tp)
                db.insert_sub_types(tp, type['sub_types'])
                for item in type['sub_types']:
                    # print(item)
                    get_guwens(tp, item, db)
        finally:
            db.release()


if __name__ == '__main__':
    main()
