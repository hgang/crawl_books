from sqlalchemy.orm import scoped_session

from DBTables import *
from sqlalchemy import create_engine

engine = create_engine('sqlite:///' + DB_NAME)
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker()
# DBSession = scoped_session(
#     sessionmaker(
#         autocommit=False,
#         autoflush=False,
#         bind=engine
#     )
# )
DBSession.bind = engine
session = DBSession()
