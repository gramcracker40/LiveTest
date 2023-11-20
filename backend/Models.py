'''
This file implements all of the database objects for the backend of the app
using sqlalchemy. 

A Model is simply one of the classes below inheriting from 'Base'. They are 
tables in the database that are queryable. The API will implements routes for
manipulation of all of these objects in routers/.
'''

from sqlalchemy import Column, LargeBinary, Table, Integer, \
        DateTime, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# build all of the necessary SQL database tables

class Scantron(Base):
    __tablename__ = 'scantron'
    id = Column(Integer, primary_key=True)

    graded_photo = Column(LargeBinary, nullable=False)
    num_questions = Column(Integer)
    answers = Column(String, nullable=False) # JSON string produced by 
                             # grade_answers in ScantronProcessor
    grade = Column(Float, nullable=False)
    
    # correlate the scantron to a student
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)  # Foreign key reference
    student = relationship('Student', back_populates='scantrons')

    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    test = relationship('Test', back_populates='scantrons')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    courses = relationship('Course', back_populates='teacher')

# many to many relationship
students_courses_association = Table(
    'students_courses_association', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    M_number = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True) # differentiator for duplicates.
    password = Column(String)
    
    # relationships
    scantrons = relationship('Scantron', back_populates='student')
    courses = relationship('Course', secondary=students_courses_association, back_populates='students')


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)           # 1 (unique primary ID)
    name = Column(String, nullable=False)            # Programming Language Concepts
    course_number = Column(String, nullable=False)   # 4143 PLC
    semester_season = Column(String, nullable=False) # Fall or Spring, Summer 1, Summer 2
    year = Column(Integer, nullable=False)           # 2023
    
    # relationships with others tables. 
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher', back_populates='courses')
    
    tests = relationship('Test', back_populates='course')
    students = relationship('Student', secondary=students_courses_association, back_populates='courses')


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    
    # should be a datetime object
    start_t = Column(DateTime)
    end_t = Column(DateTime)

    num_questions = Column(Integer)
    answer_key = Column(LargeBinary, nullable=False)

    # relationships
    scantrons = relationship('Scantron', back_populates='test')
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='tests')
    
