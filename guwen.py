from SubTypeParser import *
from DBHelper import *

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


def get_guwens(type, sub_type):
    subParser = SubTypeParser(type, sub_type)
    subParser.start_parse()


def main():
    # get_guwens('小说家类')
    types = get_guwen_types();
    for type in types:
        tp = type['type']
        session.add(Type(tp))
        session.add_all([SubType(tp, item) for item in type['sub_types']])
        for item in type['sub_types']:
            # print(item)
            get_guwens(tp, item)

        session.commit()


if __name__ == '__main__':
    main()
