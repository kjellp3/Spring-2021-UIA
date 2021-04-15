from actions import *


def main():
    print(
        "1. Read all students\n"
        "2. Get student by id\n"
        "3. Add student\n"
        "4. Edit student\n"
        "5. Remove student\n"
        "6. Exit")
    while True:

        command = int(input())

        if command == 1:
            read_all()
        elif command == 2:
            stud_by_id()
        elif command == 3:
            add_student()
        elif command == 4:
            edit_student()
        elif command == 5:
            delete()
        else:
            break


if __name__ == '__main__':
    main()
