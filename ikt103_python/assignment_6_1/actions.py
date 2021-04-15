import requests

URL = "http://localhost:5000/students/"


def read_all():
    response = requests.get(URL)
    for student in response.json():
        for key, value in student.items():
            if key == 'year':
                print(f"{key}: {value}")
            else:
                print(f"{key}: {value}", end=", ")


def stud_by_id():
    response = requests.get(URL + input("Id: "))
    if response.status_code == 200:
        for key, value in response.json().items():
            if key == 'year':
                print(f"{key}: {value}")
            else:
                print(f"{key}: {value}", end=", ")
    elif response.status_code == 404:
        print("Student not found")
    else:
        print(response.status_code)


def add_student():
    student = \
        {
            "id": requests.get(URL.replace("students/","nextId")).json()['nextId'],
            "name": input("Name: "),
            "email": input("Email: "),
            "year": int(input("Year: "))
        }
    response = requests.post(URL, json=student)
    if response.status_code == 201:
        print(f"Added student: id: {student['id']}, name: {student['name']}, email: {student['email']}, year: {student['year']}")
    else:
        print(response.status_code)


def edit_student():
    student = \
        {
            "id": int(input("Id: ")),
            "name": input("Name: "),
            "email": input("Email: "),
            "year": int(input("Year: "))
        }
    response = requests.put(URL+str(student['id']), json=student)
    if response.status_code == 200:
        print("Student was edited successfully")
    elif response.status_code == 404:
        print("Student not found")
    else:
        print(response.status_code)


def delete():
    response = requests.delete(URL + input('Id: '))
    if response.status_code == 204:
        print("Student was removed successfully")
    elif response.status_code == 404:
        print("Student not found")
    else:
        print(response.status_code)
