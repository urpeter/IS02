from flask import Flask
import json
from collections import defaultdict
from os import path


def create_application():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdgsdgsdg sadghrdtf'
    from website.views import views
    from website.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def build_food_database(data_path):
    print(f"------Building Database------")
    food_database = defaultdict(dict)
    tracked_nutrients = [1008,1003, 1005, 1004] # kcal,Protein, Carbohydrates,total Fat

    with open(data_path) as data:
        f = json.load(data)
        for fooditem in f["FoundationFoods"]:
            name = (fooditem["description"].split(","))[0]
            food_database[name]= {elem["nutrient"]['name']: elem["amount"] for elem in fooditem["foodNutrients"]if elem["nutrient"]['id'] in tracked_nutrients}

    with open("website/Databases/food_kcal_database.json", "w") as kcal_saved:
            kcal_saved.write(json.dumps(food_database,indent=4))
    return food_database


def initialize():
    if not path.exists("website/Databases/food_kcal_database.json"):
        food_db = build_food_database("FoodData_Central_foundation_food_json_2022-04-28.json")
    else :
        with open("website/Databases/food_kcal_database.json") as d:
            food_db = json.load(d)
    return food_db