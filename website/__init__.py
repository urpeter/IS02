from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from collections import defaultdict
from os import path
from flask_login import LoginManager

# food_db = SQLAlchemy()
# food_DB_NAME = 'food_data.db'
user_db = SQLAlchemy()
user_DB_NAME = 'user_data.db'


def create_application():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdgsdgsdg sadghrdtf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{user_DB_NAME}'
    # app.config['SQLALCHEMY_BINDS'] = {"food_db": f'sqlite:///{food_DB_NAME}'}
    user_db.init_app(app)

    from website.views import views
    from website.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Food
    initialize(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def build_food_database(data_path):
    print(f"------Building Database------")
    food_database = defaultdict(dict)
    tracked_nutrients = [1008, 1003, 1005, 1004]  # kcal,Protein, Carbohydrates,total Fat

    with open(data_path) as data:
        f = json.load(data)
        for fooditem in f["FoundationFoods"]:
            name = (fooditem["description"].split(","))[0]
            food_database[name] = {elem["nutrient"]['name']: elem["amount"] for elem in fooditem["foodNutrients"]
                                   if elem["nutrient"]['id'] in tracked_nutrients}

    with open("website/Databases/food_kcal_database.json", "w") as kcal_saved:
        kcal_saved.write(json.dumps(food_database, indent=4))
    return food_database

def initialize(application):
    if not path.exists(f"website/{user_DB_NAME}"):
        user_db.create_all(app=application)
        # food_db = build_food_database("website/Databases/food_kcal_database.json")

    return
