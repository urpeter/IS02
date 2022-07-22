from flask_login import UserMixin
from . import user_db

class Food(user_db.Model):
    id = user_db.Column(user_db.Integer, primary_key = True)
    name = user_db.Column(user_db.String(150), unique= True)
    Protein = user_db.Column(user_db.Float)
    Fat = user_db.Column(user_db.Float)
    Carbohydrate = user_db.Column(user_db.Float)
    Energy = user_db.Column(user_db.Float)

class User(user_db.Model, UserMixin):
    id = user_db.Column(user_db.Integer, primary_key= True)
    name= user_db.Column(user_db.String(150),unique=True)
    age = user_db.Column(user_db.Float)
    weight = user_db.Column(user_db.Float)
    height =user_db.Column(user_db.Float)
    goal = user_db.Column(user_db.String(150))
    sex =  user_db.Column(user_db.String(150))
    activity = user_db.Column(user_db.Float)
    kcal_intake = user_db.Column(user_db.Float)
    current_intake = user_db.Column(user_db.Float)