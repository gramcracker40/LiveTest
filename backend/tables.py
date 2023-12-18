'''
This file implements all of the database objects for the backend of the app
using sqlalchemy. 

below are tables in the database that are queryable. The API will implements routes for
manipulation of all of these objects in routers/.

main tables for the backend are 
#   Submission
#   Course
#   Test
#   Teacher 
#   Student
'''

from sqlalchemy import Column, LargeBinary, Integer, \
       DateTime, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    courses = relationship('Course', back_populates='teacher')

# many to many relationship

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    __table_args__ = (UniqueConstraint('student_id', 'course_id'),)

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    M_number = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True) # differentiator for duplicates.
    password = Column(String)
    
    # relationships
    submissions = relationship('Submission', back_populates='student')
    courses = relationship('Course', secondary=Enrollment.__table__, back_populates='students')


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
    students = relationship('Student', secondary=Enrollment.__table__, back_populates='courses')


class Submission(Base):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True)

    graded_photo = Column(LargeBinary, nullable=False)
    num_questions = Column(Integer)
    answers = Column(String, nullable=False) # JSON string produced by 
                             # grade_answers in SubmissionProcessor
    grade = Column(Float, nullable=False)
    
    # correlate the submission to a student
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)  # Foreign key reference
    student = relationship('Student', back_populates='submissions')

    test_id = Column(String, ForeignKey('tests.id'), nullable=False)
    test = relationship('Test', back_populates='submissions')


class Test(Base):
    __tablename__ = 'tests'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    # should be a datetime object
    start_t = Column(DateTime)
    end_t = Column(DateTime)
    num_questions = Column(Integer)
    answer_key = Column(LargeBinary, nullable=False)

    # relationships
    submissions = relationship('Submission', back_populates='test')
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='tests')
    
