from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from  config import *

Base = declarative_base()


# 定义类型对象:
class Type(Base):
    # 表的名字:
    __tablename__ = 'types'

    # 表的结构:
    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20))

    def __init__(self, type):
        self.type = type


# 定义子类型对象:
class SubType(Base):
    # 表的名字:
    __tablename__ = 'sub_types'

    # 表的结构:
    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20))
    sub_type = Column(String(20))

    def __init__(self, type, sub_type):
        self.type = type
        self.sub_type = sub_type


# 定义书籍对象:
class Book(Base):
    # 表的名字:
    __tablename__ = 'books'

    # 表的结构:
    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20))
    sub_type = Column(String(20))
    cover = Column(String(256))
    title = Column(String(50))
    detail_link = Column(String(256))
    author = Column(String(50))
    favorite = Column(Integer)
    score = Column(Float)
    score_count = Column(Integer)
    introduce = Column(Text)
    finished = Column(Boolean, default=False)

    def __init__(self, type, sub_type):
        self.type = type
        self.sub_type = sub_type


# 定义目录对象:
class Content(Base):
    # 表的名字:
    __tablename__ = 'contents'

    # 表的结构:
    _id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books._id'))  # 书籍id
    season = Column(String(50))  # 卷名
    chapter = Column(String(50))  # 目录名
    position = Column(Integer)  # 目录顺序
    detail_link = Column(String(256))  # 详细链接
    data = Column(Text)  # 内容
    interpret = Column(Text)  # 翻译
    analyze = Column(Text)  # 赏析

    def __init__(self, book_id):
        self.book_id = book_id


engine = create_engine('sqlite:///' + DB_NAME, echo=True)
Base.metadata.create_all(engine)
