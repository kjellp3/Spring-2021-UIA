from model.sqlclasses import Users, Cars, RentedCars
from sqlalchemy import create_engine, extract, between, update, delete
from sqlalchemy.orm import sessionmaker


# Creates a engine for all the models to inherit

class Engine:
    def __init__(self):
        self.engine = create_engine('sqlite:///rent_cars.sqlite', connect_args={'check_same_thread': False})
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.session.execute('PRAGMA foreign_keys = ON;')


# Handles all the query's for users
class UserModel(Engine):
    def get_all_users(self):
        return self.session.query(Users).all()

    def get_user_by_id(self, user_id):
        return self.session.query(Users).filter(user_id == Users.id).all()

    def get_user_by_address(self, address):
        return self.session.query(Users).filter(Users.address.ilike(f'%{address}%')).all()

    def get_user_by_age(self, span, today):
        return self.session.query(Users).filter(between(Users.birth, span, today)).all()

    def get_user_by_name(self, name):
        return self.session.query(Users).filter(Users.name.ilike(f'%{name}%')).all()

    def get_user_by_phone(self, phone):
        return self.session.query(Users).filter(Users.phone.ilike(f'%{phone}%')).all()

    def post_user(self, user):
        user = Users(name=user['name'], address=user['address'], phone=user['phone'], birth=user["birth"])
        self.session.add(user)
        self.session.commit()
        return self.session.query(Users).filter(user.id == Users.id).all()

    def put_user(self, user):
        self.session.execute(update(Users, values=user).where(Users.id == user["id"]))
        self.session.commit()
        return self.session.query(Users).filter(user["id"] == Users.id).all()

    def delete_user(self, user_id):
        self.session.execute(delete(Users).where(Users.id == user_id))
        self.session.commit()
        return '{Deleted user with id: %i}' % int(user_id)


# Handles all the query's for cars
class CarModel(Engine):
    def get_all_cars(self):
        return self.session.query(Cars).all()

    def check_reg_absolute(self, reg):
        return self.session.query(Cars).filter(reg == Cars.reg_number).all()

    def get_car_by_reg(self, reg):
        return self.session.query(Cars).filter(Cars.reg_number.ilike(f'%{reg}%')).all()

    def get_car_by_year(self, year):
        return self.session.query(Cars).filter(year == Cars.year).all()

    def get_car_by_model(self, model):
        return self.session.query(Cars).filter(Cars.model.ilike(f'%{model}%')).all()

    def get_car_by_price(self, price):
        return self.session.query(Cars).filter(Cars.price == price).all()

    def get_car_by_price_range(self, start_price, end_price):
        return self.session.query(Cars).filter(between(Cars.price, start_price, end_price)).all()

    def post_car(self, car):
        new_car = Cars(reg_number=car['reg_number'], year=car['year'], model=car['model'], price=car['price'])
        self.session.add(new_car)
        self.session.commit()
        return self.session.query(Cars).filter(car['reg_number'] == Cars.reg_number).all()

    def put_car(self, car, reg_number):
        self.session.execute(update(Cars, values=car).where(Cars.reg_number == reg_number))
        self.session.commit()
        return self.session.query(Cars).filter(car["reg_number"] == Cars.reg_number).all()

    def delete_car(self, reg):
        self.session.execute(delete(Cars).where(Cars.reg_number == reg))
        self.session.commit()
        return '{Deleted Car with registration number: %s}' % reg


# Handles all the query's for renting
class RentalModel(Engine):
    def get_all_rentals(self):
        return self.session.query(RentedCars).all()

    def get_rental_by_id(self, rental_id):
        return self.session.query(RentedCars).filter(RentedCars.id == rental_id).all()

    def get_rental_by_userid(self, user_id):
        return self.session.query(RentedCars).filter(RentedCars.user_id == user_id).all()

    def get_rental_by_reg(self, reg):
        return self.session.query(RentedCars).filter(RentedCars.reg_number.ilike(f'%{reg}%')).all()

    def get_rental_by_time(self, rent_from, rent_to):
        if len(list(rent_to)) == 4:
            return self.session.query(RentedCars).filter(
                between(extract('year', RentedCars.rent_from), rent_from, rent_to) |
                between(extract('year', RentedCars.rent_to), rent_from, rent_to)).all()

        else:
            return self.session.query(RentedCars).filter(between(RentedCars.rent_from, rent_from, rent_to) |
                                                         between(RentedCars.rent_to, rent_from, rent_to)).all()

    def check_user_id(self, user_id):
        return self.session.query(Users).get(user_id)

    def check_reg_absolute(self, reg):
        return self.session.query(Cars).filter(reg == Cars.reg_number).all()

    def check_if_available_post(self, rent):
        return self.session.query(RentedCars).filter(
            between(rent['rent_from'], RentedCars.rent_from, RentedCars.rent_to) |
            between(rent['rent_to'], RentedCars.rent_from, RentedCars.rent_to) |
            between(RentedCars.rent_from, rent['rent_from'], rent['rent_to']) |
            between(RentedCars.rent_to, rent['rent_from'], rent['rent_to'])) \
            .filter(RentedCars.reg_number == rent['reg_number']).all()

    def check_if_available_put(self, rent, rental_id):
        return self.session.query(RentedCars).filter(
            between(rent['rent_from'], RentedCars.rent_from, RentedCars.rent_to) |
            between(rent['rent_to'], RentedCars.rent_from, RentedCars.rent_to) |
            between(RentedCars.rent_from, rent['rent_from'], rent['rent_to']) |
            between(RentedCars.rent_to, rent['rent_from'], rent['rent_to'])) \
            .filter(RentedCars.reg_number == rent['reg_number']) \
            .filter(RentedCars.id != rental_id).all()

    def post_rental(self, rent):
        user = self.session.query(Users).get(rent['user_id'])

        car_rental = RentedCars(rent_from=rent['rent_from'], rent_to=rent['rent_to'], price_tot=rent['price_tot'])

        car_rental.car = self.session.query(Cars).filter(Cars.reg_number == rent['reg_number']).one()

        user.cars.append(car_rental)

        self.session.commit()
        return self.session.query(RentedCars).order_by(RentedCars.id.desc()).first()

    def put_rental(self, rent, rental_id):
        self.session.query(RentedCars).filter(RentedCars.id == rental_id).update(rent)
        self.session.commit()
        return self.session.query(RentedCars).filter(rental_id == RentedCars.id).all()

    def delete_rental(self, rental_id):
        self.session.query(RentedCars).filter(RentedCars.id == rental_id).delete()
        self.session.commit()
        return '{Successfully deleted rental with id: %s}' % rental_id
