from controller.usershandler import GetUsers
from controller.carshandler import GetCars
from controller.rentalshandler import Rental
from flask import Flask
from flask_restful import Api


def main():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(GetUsers,
                     '/users/',
                     '/users/id/<user_id>',
                     '/users/address/<address>',
                     '/users/phone/<phone>',
                     '/users/name/<name>',
                     '/users/age/<age>')

    api.add_resource(GetCars,
                     '/cars/model/<model>',
                     '/cars/reg_number/<reg_number>',
                     '/cars/reg_number_absolute/<reg_number_absolute>',
                     '/cars/year/<year>',
                     '/cars/')

    api.add_resource(Rental,
                     '/rental/',
                     '/rental/user_id/<user_id>',
                     '/rental/time/<rent_from>/<rent_to>',
                     '/rental/reg_number/<reg_number>',
                     '/rental/id/<rental_id>')


    # I decided to run on 127.0.0.2 instead of localhost because of performance issues
    app.run(debug=True, port=5000, host='127.0.0.2')


if __name__ == '__main__':
    main()
