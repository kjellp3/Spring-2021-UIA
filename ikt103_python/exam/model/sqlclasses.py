from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class RentedCars(Base):
    __tablename__ = 'rentedcars'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    reg_number = Column('reg_number', String, ForeignKey('cars.reg_number'))
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    rent_from = Column('rent_from', DATETIME)
    rent_to = Column('rent_to', DATETIME)
    price_tot = Column('price_tot', Integer)

    car = relationship('Cars', back_populates='users', lazy=True)
    user = relationship('Users', back_populates='cars', lazy=True)


class Cars(Base):
    __tablename__ = 'cars'
    reg_number = Column('reg_number', String, primary_key=True, onupdate='cascade')
    year = Column('year', Integer)
    model = Column('model', String)
    price = Column('price', Integer)

    users = relationship('RentedCars', back_populates='car', lazy='joined')


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, onupdate='cascade')
    address = Column('address', String)
    phone = Column('phone', String)
    name = Column('name', String)
    birth = Column('birth', DATE)

    cars = relationship('RentedCars', back_populates='user', lazy='joined')

