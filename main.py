import ast
import gpiozero
import signal
import requests
import json
import argparse
from collections import defaultdict
from flask import Flask, render_template, jsonify, request

###### User Settings ########
with open("Databases/user_database.txt","r") as u_d:
    user_database = ast.literal_eval(u_d.read())
app = Flask(__name__)
class UserProfile():
    def __init__(self,name, age, weight, height, goal, sex, activity):
        self.id = len(user_database) + 1
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.goal = goal
        self.sex = sex
        self.activity = activity # should be 1.2 , 1.5 or 1.7
        self.kcal_intake = 0
        self.calorie_goal = self.set_calorie_goal()

    def update_user(self, parameters):
        for parameter in parameters:
            self.name = parameter[1]
            self.age = parameter[2]
            self.weight = parameter[3]
            self.height = parameter[4]
            self.goal = parameter[5]
            self.sex = parameter[6]
            self.kcal_intake = parameter[7]
            self.calorie_goal = parameter[8]

    def set_calorie_goal(self):
        if self.sex == "female":
            bmr = (self.weight * 10.0 + self.height * 6.25 - self.age * 5.0 - 161.0) * self.activity
        else:
            bmr = (self.weight * 10.0 + self.height * 6.25 - self.age * 5.0 + 5.0) * self.activity

        if self.goal == "loss":
            goal = bmr - 500.0
        elif self.goal == "gain":
            goal = bmr + 500.0
        else:
            goal = bmr
        return goal

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)

####### Requests #########
@app.get("/user_database")
def get_countries():
    user_jsonbase = [ json.loads(x.toJSON()) for x in user_database]
    #print(user_jsonbase)
    return jsonify(user_jsonbase)

@app.put('/user_database')
def create_user():
    if request.is_json:
        nur = request.get_json()
        new_user = UserProfile(nur["name"], nur["age"], nur["weight"], nur["height"], nur["goal"], nur["sex"], nur["activity"])
        user_database.append(new_user)
        with open("Databases/user_database.txt", "w") as u_d:
            u_d.write(str(user_database))
        #response = requests.put("/Databases/user_database",json=new_user.toJSON())
        return new_user.toJSON(), 201
    return {"TypeError:":"Request is not JSON"},415

##### building database ########
#TODO add database for users own products only
class FoodItem():
    def __init__(self, name, nutrients):
        self.name = name
        self.calorie_amount = nutrients
def build_food_database(data_path):
    print(f"------Building Databse-------")
    kcal_database = defaultdict()
    with open(data_path) as data:
        f = json.load(data)
        for fooditem in f["FoundationFoods"]:
            kcal_database[(fooditem["description"].split(","))[0]] = list(filter(lambda x: x != '', [elem["amount"] if ('kcal' == elem["nutrient"]['unitName']) else '' for elem in fooditem["foodNutrients"]]))[0]

    with open("Databases/food_kcal_database.txt", "w") as kcal_saved:
            kcal_saved.write(str(kcal_database))
    return kcal_database


###### System Settings #######
def initialize():
    if args["init"] == True:
        cal_data = build_food_database("FoodData_Central_foundation_food_json_2022-04-28.json")
    else:
        with open("Databases/food_kcal_database.txt") as d:
            cal_data = ast.literal_eval(d.read())
    return cal_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse the arguments to setup the scale")
    parser.add_argument('--init', action="store_true" ,help="initializes the Database")
    parser.add_argument('--flask', action="store_true")
    args = vars(parser.parse_args())
    if args['flask']:
        @app.route("/")
        def home():
            return render_template('bla.html')
    app.run()
    food_database = initialize()
    #active_scale = False

    #while active_scale:
     #   pass


