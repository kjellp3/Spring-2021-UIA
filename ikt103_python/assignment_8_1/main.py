from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from operations import *





def main():
    engine = create_engine('sqlite:///school.sqlite')
    Session = sessionmaker(bind=engine)

    session = Session()

    print("1. Add student\n"
          "2. Add course\n"
          "3. Add test\n"
          "4. Add student to course\n"
          "5. List courses by student\n"
          "6. List tests by course\n"
          "7. Exit")

    while True:
        action = int(input())

        if action == 1:
            add_student(session)
        elif action == 2:
            add_course(session)
        elif action == 3:
            add_test(session)
        elif action == 4:
            add_student_to_course(session)
        elif action == 5:
            list_courses_by_student(session)
        elif action == 6:
            list_tests_by_course(session)
        elif action == 7:
            break
        else:
            print("Invalid operation")




if __name__ == '__main__':
    main()

