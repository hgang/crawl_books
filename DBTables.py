from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 定义类型对象:
class Type(Base):
    # 表的名字:
    __tablename__ = 'types'

    # 表的结构:
    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20))


# 定义子类型对象:
class SubType(Base):
    # 表的名字:
    __tablename__ = 'sub_types'

    # 表的结构:
    _id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20))
    sub_type = Column(String(20))


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


# 定义目录对象:
class Content(Base):
    # 表的名字:
    __tablename__ = 'contents'

    # 表的结构:
    _id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'))  # 书籍id
    title = Column(String(50))  # 目录名
    detail_link = Column(String(256))  # 详细链接
    data = Column(Text)  # 内容
    interpret = Column(Text)  # 翻译
    analyze = Column(Text)  # 赏析


engine = create_engine('sqlite:///foo.db', echo=True)
Base.metadata.create_all(engine)
