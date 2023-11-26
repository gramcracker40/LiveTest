'''
Sets up the backends database session manager
'''

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from tables import Base
from env import database_url

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
