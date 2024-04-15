"""
This file implements all of the database tables for the backend of the app

below are tables in the database that are queryable. The API will implements routes for
CRUD manipulation of all of these objects in routers/.

main tables for the backend are 
#   Submission
#   Course
#   Test
#   Teacher 
#   Student
"""

from sqlalchemy import (
    Column,
    LargeBinary,
    Integer,
    DateTime,
    String,
    Float,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    courses = relationship("Course", back_populates="teacher")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    __table_args__ = (UniqueConstraint("student_id", "course_id"),)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)  # differentiator for duplicates.
    password = Column(String)

    # relationships
    submissions = relationship("Submission", back_populates="student")
    courses = relationship(
        "Course", secondary=Enrollment.__table__, back_populates="students"
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)  # 1 (unique primary ID)
    name = Column(String, nullable=False)  # Programming Language Concepts
    section = Column(Integer, nullable=False)
    course_number = Column(Integer, nullable=False)  # 4143 PLC
    semester_season = Column(
        String, nullable=False
    )  # Fall or Spring, Summer 1, Summer 2
    year = Column(Integer, nullable=False)  # 2023
    subject = Column(String, nullable=False)

    # relationships with others tables.
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="courses")

    tests = relationship("Test", back_populates="course")
    students = relationship(
        "Student", secondary=Enrollment.__table__, back_populates="courses"
    )

    # If all of these values are the same, it should constitute as a duplicate
    __table_args__ = (
        UniqueConstraint("section", "course_number", "name", "semester_season", "year"),
    )


class Submission(Base):
    __tablename__ = "submission"
    id = Column(Integer, primary_key=True)

    submission_image = Column(LargeBinary, nullable=False)
    graded_image = Column(LargeBinary, nullable=False)

    answers = Column(String, nullable=False)  # JSON string produced by
    # grade_answers in SubmissionProcessor
    grade = Column(Float, nullable=False)

    # correlate the submission to a student
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    student = relationship("Student", back_populates="submissions")

    test_id = Column(String, ForeignKey("tests.id"), nullable=False)
    test = relationship("Test", back_populates="submissions")

    __table_args__ = (
        CheckConstraint("student_id", "test_id"), # ensures single submission
    )


class Test(Base):
    __tablename__ = "tests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    start_t = Column(DateTime)
    end_t = Column(DateTime)
    num_questions = Column(Integer, nullable=False)
    num_choices = Column(Integer, nullable=False)
    
    answers = Column(String, nullable=False)
    answer_key_blank = Column(LargeBinary, nullable=False)
    answer_key_filled = Column(LargeBinary, nullable=False)

    # relationships
    submissions = relationship("Submission", back_populates="test", cascade="all, delete")
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="tests")

    __table_args__ = (UniqueConstraint("course_id", "name"),)
