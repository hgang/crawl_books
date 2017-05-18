from DBTables import *
from sqlalchemy import create_engine

engine = create_engine('sqlite:///foo.db')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
