from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    year = Column(Integer)


class Courses(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    max_students = Column(Integer)


class Tests(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    name = Column(String)
    date_time = Column(String)


class StudentCourses(Base):
    __tablename__ = 'students_courses'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)




def add_student(session):
    new_student = Students(name=input('Name: '), email=input('Email: '), year=input('Year: '))
    session.add(new_student)
    session.commit()
    print(f'Added student with id {new_student.id}')


def add_course(session):
    new_course = Courses(name=input('Name: '), max_students=input('Max students: '))
    session.add(new_course)
    session.commit()
    print(f'Added course with id {new_course.id}')


def add_test(session):
    new_test = Tests(course_id=input('Course id: '), name=input('Name: '), date_time=input('Date time: '))
    session.add(new_test)
    session.commit()
    print(f'Added test with id {new_test.id}')


def add_student_to_course(session):
    student_id = input('Id: ')
    if not session.query(Students).filter(Students.id == student_id).all():
        print('Student not found')
        return -1

    course_id = input('Course id: ')
    if not session.query(Courses).filter(Courses.id == course_id).all():
        print('Course not found')
        return -1

    new_student_course = StudentCourses(student_id=student_id, course_id=course_id)
    session.add(new_student_course)
    session.commit()
    print(f'Added student to course id {course_id}')



def list_courses_by_student(session):
    student_id = input('Id: ')
    if not session.query(Students).filter(Students.id == student_id).all():
        print('Student not found')
        return -1

    student_courses = session.query(Courses).join(StudentCourses).filter(StudentCourses.student_id == student_id).order_by(Courses.id).all()
    print(f'Courses for student {student_id}: {", ".join([course.name for course in student_courses])}')


def list_tests_by_course(session):
    course_id = input('Course id: ')
    if not session.query(Courses).filter(Courses.id == course_id).all():
        print('Course not found')
        return -1

    course_tests = session.query(Tests).join(Courses).filter(Tests.course_id == course_id).order_by(Tests.id).all()
    print(f'Tests for course {course_id}: {", ".join([course.name for course in course_tests])}')






















