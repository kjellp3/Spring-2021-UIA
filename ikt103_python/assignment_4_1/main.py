from school import Student
import json


def main():
    with open("students.json") as data:
        stud_list = sorted([Student(i['name'],i['age'],i['attendance']) for i in json.load(data)],key=Student.sort_age)

    [print(f"Youngest: {stud_list[i].name}") for i in range(len(stud_list)) if stud_list[i].age == stud_list[0].age]
    [print(f"Oldest: {stud_list[i].name}") for i in range(len(stud_list)) if stud_list[i].age == stud_list[-1].age]
    print(f"Average age: {Student.average_age(stud_list)}")
    [print(f"Bad student: {stud.name}")for stud in stud_list if stud.badStudent]


if __name__ == '__main__':
    main()
