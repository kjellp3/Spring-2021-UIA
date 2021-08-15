from model.querys import UserModel
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from controller.handelhelper import post_user



class GetUsers(Resource, UserModel):
    def get(self, user_id=None, address=None, phone=None, name=None, age=None):
        if user_id is not None:
            users = self.get_user_by_id(user_id)
            if not users:
                raise NotFound(f'No users with id: {user_id} exist')
        elif address is not None:
            users = self.get_user_by_address(address)
            if not users:
                raise NotFound(f'No addresses found for {address}')
        elif phone is not None:
            users = self.get_user_by_phone(phone)
            if not users:
                raise NotFound(f'No users with phone number {phone} exist')
        elif name is not None:
            users = self.get_user_by_name(name)
            if not users:
                raise NotFound(f'No users with name: {name} exist')
        elif age is not None:
            birth = datetime.now() - relativedelta(years=int(age))
            span = datetime.now() - relativedelta(years=1+int(age))
            users = self.get_user_by_age(today=birth.date(), span=span.date())
            if not users:
                raise NotFound(f'No users with age: {age} found')
        else:
            users = self.get_all_users()

        return post_user.dump(users)

    def post(self):
        user = request.get_json()
        user["birth"] = datetime.strptime(user["birth"], '%Y-%m-%d')
        return post_user.dump(self.post_user(user))

    def put(self, user_id):
        if not self.get_user_by_id(user_id):
            raise NotFound('User id does not exist')
        user = request.get_json()
        user["birth"] = datetime.strptime(user["birth"], '%Y-%m-%d')
        return post_user.dump(self.put_user(user))

    def delete(self, user_id):
        if not self.get_user_by_id(user_id):
            raise NotFound('User id does not exist')
        return self.delete_user(user_id)