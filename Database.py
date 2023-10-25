from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Models import Student, Scantron, Teacher, Course, Test, Base


db_url = "sqlite:///scantron-hacker.db"  # SQLite database URL
engine = create_engine(db_url)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# example using filters. A lot more precise ways of filtering the data using the session object
# searching_student_id = 4
# new_scantron = session.query(Scantron).filter(Scantron.student_id == searching_student_id)

# example
# new_student = Student(name="garreyy")
# session.add(new_student)
# session.commit()



