from sqlalchemy import Column, LargeBinary, Table, Integer, \
        DateTime, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

students_courses_association = Table(
    'students_courses_association', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Scantron(Base):
    __tablename__ = 'scantron'
    id = Column(Integer, primary_key=True)
    
    num_questions = Column(Integer)
    answers = Column(String, nullable=False) # JSON string produced by 
                             # grade_answers in ScantronProcessor
    grade = Column(Float, nullable=False)
    
    # correlate the scantron to a student
    student_id = Column(Integer, ForeignKey('students.id'))  # Foreign key reference
    student = relationship('Student', back_populates='scantrons')

    test_id = Column(Integer, ForeignKey('tests.id'))
    test = relationship('Test', back_populates='scantrons')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    courses = relationship('Course', back_populates='teacher')

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    scantrons = relationship('Scantron', back_populates='student')
    courses = relationship('Course', secondary=students_courses_association, back_populates='students')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    course_number = Column(String, nullable=False)
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher', back_populates='courses')
    tests = relationship('Test', back_populates='course')
    students = relationship('Student', secondary=students_courses_association, back_populates='courses')


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    start_t = Column(DateTime)  # You may want to use a Date type
    end_t = Column(DateTime)
    questions = Column(Integer)
    key = Column(LargeBinary, nullable=False)

    scantrons = relationship('Scantron', back_populates='test')

    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='tests')
    
