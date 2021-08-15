import requests


# Names this file prayer because it handles all the prayers to the database


BASE_URL = 'http://127.0.0.2:5000/'


def users(get=False, post=False, delete=False, put=False, name=None, user_id=None, age=None, address=None, phone=None, json=None):

    if get:
        if name is None and user_id is None and age is None and address is None and phone is None:
            return requests.get(f'{BASE_URL}users').json()
        elif name is not None:
            return requests.get(f'{BASE_URL}users/name/{name}').json()
        elif user_id is not None:
            return requests.get(f'{BASE_URL}users/id/{user_id}').json()
        elif age is not None:
            return requests.get(f'{BASE_URL}users/age/{age}').json()
        elif address is not None:
            return requests.get(f'{BASE_URL}users/address/{address}').json()
        elif phone is not None:
            return requests.get(f'{BASE_URL}users/phone/{phone}').json()

    elif post:
        return requests.post(f'{BASE_URL}users/', json=json).json()
    elif put:
        return requests.put(f'{BASE_URL}users/id/{json["id"]}', json=json).json()
    elif delete:
        return requests.delete(f'{BASE_URL}users/id/{user_id}').json()


def cars(get=False, post=False, delete=False, put=False, reg=None, reg_absolute=None, model=None, year=None, json=None):
    if get:
        if reg is None and model is None and year is None and reg_absolute is None:
            return requests.get(f'{BASE_URL}cars/').json()
        if reg is not None:
            return requests.get(f'{BASE_URL}cars/reg_number/{reg}').json()
        elif reg_absolute is not None:
            return requests.get(f'{BASE_URL}/cars/reg_number_absolute/{reg_absolute}')
        elif model is not None:
            return requests.get(f'{BASE_URL}cars/model/{model}').json()
        elif year is not None:
            return requests.get(f'{BASE_URL}cars/year/{year}').json()

    elif post:
        return requests.post(f'{BASE_URL}cars/', json=json).json()
    elif put:
        return requests.put(f'{BASE_URL}cars/reg_number/{reg}', json=json).json()
    elif delete:
        return requests.delete(f'{BASE_URL}cars/reg_number/{reg}').json()


def rentals(get=False, post=False, put=False, delete=False, user_id=None, reg=None, rental_id=None, rfrom=None, rto=None, json=None):
    if get:
        if user_id is None and reg is None and rental_id is None and rfrom is None and rto is None:
            return requests.get(f'{BASE_URL}rental/').json()
        elif user_id is not None:
            return requests.get(f'{BASE_URL}rental/user_id/{user_id}').json()
        elif reg is not None:
            return requests.get(f'{BASE_URL}rental/reg_number/{reg}').json()
        elif rental_id is not None:
            return requests.get(f'{BASE_URL}rental/id/{rental_id}').json()
        elif rfrom is not None and rto is not None:

            return requests.get(f'{BASE_URL}rental/time/{rfrom}/{rto}').json()
        elif rfrom is not None:
            return requests.get(f'{BASE_URL}rental/time/{rfrom}').json()
    elif post:
        return requests.post(f'{BASE_URL}rental/', json=json).json()
    elif put:
        return requests.put(f'{BASE_URL}rental/id/{json["id"]}', json=json).json()
    elif delete:
        return requests.delete(f'{BASE_URL}rental/id/{rental_id}').json()
