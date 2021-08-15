from model.querys import RentalModel
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import *
from datetime import datetime
from controller.handelhelper import post_rental


class Rental(Resource, RentalModel):
    def get(self, reg_number=None, user_id=None, rent_from=None, rent_to=None, rental_id=None):

        if rental_id is not None:
            cars_rented = self.get_rental_by_id(rental_id)
            if not cars_rented:
                raise NotFound(f'No rentals for id: {rental_id} found')
        elif reg_number is not None:
            cars_rented = self.get_rental_by_reg(reg_number)
            if not cars_rented:
                raise NotFound(f'No rentals for car with registration number: {reg_number} found')
        elif user_id is not None:
            cars_rented = self.get_rental_by_userid(user_id)
            if not cars_rented:
                raise NotFound(f'No rentals for user with id: {user_id} found')
        elif rent_from is not None and rent_to is not None:
            cars_rented = self.get_rental_by_time(rent_from,rent_to)
            if not cars_rented:
                raise NotFound(f'No rentals for time period: {rent_from, rent_to} found')

        else:
            cars_rented = self.get_all_rentals()

        return post_rental.dump(cars_rented)

    def post(self):

        rent = request.get_json()

        rent['rent_from'] = datetime.strptime(rent['rent_from'], '%Y-%m-%d %H:%M:%S')
        rent['rent_to'] = datetime.strptime(rent['rent_to'], '%Y-%m-%d %H:%M:%S')

        if not self.check_reg_absolute(rent["reg_number"]):
            raise NotFound(f'There is no car with registration number: {rent["reg_number"]}')
        if not self.check_user_id(rent["user_id"]):
            raise NotFound(f'There is no user with id: {rent["user_id"]}')
        check = self.check_if_available_post(rent)
        if check:
            raise BadRequest('Car is already rented out within that time period.\n'
                             'It is rented out between these time periods:\n'
                             '{0}'.format('\n'.join([(str(i.rent_from) + ' and ' + str(i.rent_to)) for i in check])))
        return post_rental.dump([self.post_rental(rent)])


    def put(self, rental_id):
        if not self.get_rental_by_id(rental_id):
            raise NotFound(f'There is no rental for id: {rental_id}')
        rent = request.get_json()
        if not self.check_reg_absolute(rent["reg_number"]):
            raise NotFound(f'There is no car with registration number: {rent["reg_number"]}')
        if not self.check_user_id(rent["user_id"]):
            raise NotFound(f'There is no user with id: {rent["user_id"]}')

        rent['rent_from'] = datetime.strptime(rent['rent_from'], '%Y-%m-%d %H:%M:%S')
        rent['rent_to'] = datetime.strptime(rent['rent_to'], '%Y-%m-%d %H:%M:%S')

        check = self.check_if_available_put(rent, rental_id)

        if check:
            raise BadRequest(f'Car is already rented out within that time frame.\n'
                             f'It is rented out between {",".join([str(i.rent_from) for i in check])} and {",".join([str(i.rent_to) for i in check])}')

        return post_rental.dump(self.put_rental(rent,rental_id))


    def delete(self, rental_id):
        if not self.get_rental_by_id(rental_id):
            raise NotFound(f'Renting id: {rental_id} not found')

        return self.delete_rental(rental_id)