from model.sqlclasses import Users, Cars, RentedCars
from flask_marshmallow import Marshmallow


ma = Marshmallow()




class PostCar(ma.Schema):
    class Meta:
        fields = ("model", "reg_number", "year", "price")
        model = Cars


class PostRental(ma.Schema):
    class Meta:
        fields = ("id", "reg_number", "user_id", "rent_from", "rent_to", "price_tot")
        model = Users


class PostUser(ma.Schema):
    class Meta:
        fields = ("id", "address", "phone", "birth", "name")
        model = RentedCars


posts_car = PostCar(many=True)
post_user = PostUser(many=True)
post_rental = PostRental(many=True)
