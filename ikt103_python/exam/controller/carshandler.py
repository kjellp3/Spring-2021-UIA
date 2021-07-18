from model.querys import CarModel
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import *
from controller.handelhelper import posts_car




class GetCars(Resource, CarModel):
    def get(self, reg_number=None, reg_number_absolute=None, year=None, model=None):
        if reg_number_absolute is not None:
            cars = self.check_reg_absolute(reg_number_absolute)
            if not cars:
                raise NotFound(f'Car with registration number: {reg_number_absolute} does not exist')
        elif reg_number is not None:
            cars = self.get_car_by_reg(reg_number)
            if not cars:
                raise NotFound(f'Car with registration number: {reg_number} does not exist')
        elif year is not None:
            cars = self.get_car_by_year(year)
            if not cars:
                raise NotFound(f'No cars with registration year: {year}')
        elif model is not None:
            cars = self.get_car_by_model(model)
            if not cars:
                raise NotFound(f'No cars with model name: {model}')
        else:
            cars = self.get_all_cars()

        return posts_car.dump(cars)

    def post(self):
        car = request.get_json()
        if self.get_car_by_reg(car["reg_number"]):
            raise BadRequest('Invalid registration number car might already exists')
        return posts_car.dump(self.post_car(car))


    def put(self, reg_number):
        car = request.get_json()
        if not self.get_car_by_reg(reg_number):
            raise NotFound('Car does not exist')
        return posts_car.dump(self.put_car(car, reg_number))

    def delete(self, reg_number):
        car_status = self.get_car_by_reg(reg_number)
        if not car_status:
            raise NotFound('Car does not exist')
        return self.delete_car(reg_number)