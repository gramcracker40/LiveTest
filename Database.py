from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Models import Student, Scantron, Teacher, Course, Test, Base


db_url = "sqlite:///scantron-hacker.db"  # SQLite database URL
engine = create_engine(db_url)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# example 
new_scantron = Scantron()





# example
# new_student = Student(name="garreyy")
# session.add(new_student)
# session.commit()



