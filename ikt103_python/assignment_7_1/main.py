from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class School(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    year = Column(Integer)


def get_info(students):
    if type(students) == list:
        for student in students:
            print(f'id: {student.id}, name: {student.name}, email: {student.email}, year: {student.year}')
    else:
        print(f'id: {students.id}, name: {students.name}, email: {students.email}, year: {students.year}')


def read_all(session):
    students = session.query(School).all()

    if not students:
        print('No students found')
    else:
        get_info(students)


def get_student(session):
    student = session.query(School).filter(School.id == input('id: ')).all()
    if not student:
        print('No students found')
    else:
        get_info(student[0])


def add_student(session):
    new_student = School(name=input('Name: '), email=input('Email: '), year=input('Year: '))
    session.add(new_student)
    session.commit()
    print("Added student: ", end='')
    get_info(new_student)


def edit_student(session):
    stud_id = input('id: ')
    if not session.query(School).filter(School.id == stud_id).all():
        print('Student not found')
    else:
        session.query(School).filter(School.id == stud_id).update({School.name: input('Name: ')})
        session.query(School).filter(School.id == stud_id).update({School.email: input('Email: ')})
        session.query(School).filter(School.id == stud_id).update({School.year: int(input('Year: '))})
        session.commit()

        print('Student was edited successfully')


def remove_student(session):
    kebab = input('id: ')
    if not session.query(School).filter(School.id == kebab).all():
        print('Student not found')
    else:
        session.query(School).filter(School.id == kebab).delete()
        session.commit()
        print('Student was removed successfully')


def search(session):
    student = session.query(School).filter(School.name.like(input('Search: '))).all()
    get_info(student)


def main():
    engine = create_engine('sqlite:///school.sqlite')
    Session = sessionmaker(bind=engine)

    session = Session()

    print("1. Read all students\n"
          "2. Get student by id\n"
          "3. Add student\n"
          "4. Edit student\n"
          "5. Remove student\n"
          "6. Search\n"
          "7. Exit")

    while True:
        action = int(input())

        if action == 1:
            read_all(session)
        elif action == 2:
            get_student(session)
        elif action == 3:
            add_student(session)
        elif action == 4:
            edit_student(session)
        elif action == 5:
            remove_student(session)
        elif action == 6:
            search(session)
        elif action == 7:
            break


if __name__ == '__main__':
    main()
