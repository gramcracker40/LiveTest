'''
Sets up the backends database
also creates the session maker that allows for 
sessions to be initiated with the db and query it.
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from env import database_url
from tables import Base

engine = create_engine(database_url)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# helper to get a database session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
