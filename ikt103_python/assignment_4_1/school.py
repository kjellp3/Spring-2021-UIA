import math


class Student:
    def __init__(self, name,age,attendance):
        self.name = name
        self.age = age
        if attendance < 30:
            self.badStudent = True
        else:
            self.badStudent = False

    @staticmethod
    def average_age(student_list):
        return math.floor(sum([stud.age for stud in student_list])/len(student_list))

    @staticmethod
    def sort_age(stud):
        return stud.age
