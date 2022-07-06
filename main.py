import ast
import gpiozero
import signal
import requests
import json
import argparse
from collections import defaultdict
from flask import Flask, render_template, jsonify, request

###### User Settings ########
try:
    with open("Databases/user_database.json","r") as u_d:
        user_database = json.load(u_d)
except:
    user_database = defaultdict()

app = Flask(__name__)
def setUserProfile(name, age, weight, height, goal, sex, activity): #activity should be 1.2 , 1.5 or 1.7
    args = locals()
    new_user = {str(parameters):values for parameters, values in args.items()}
    id = len(user_database.keys()) + 1
    new_user["kcal_intake"] = 0
    new_user["calorie_goal"] = set_calorie_goal(new_user)
    return id , new_user

def set_calorie_goal(user):
    if user["sex"] == "female":
        bmr = (user["weight"] * 10.0 + user["height"] * 6.25 - user["age"] * 5.0 - 161.0) * user["activity"]
    else:
        bmr = (user["weight"] * 10.0 + user["height"] * 6.25 - user["age"] * 5.0 + 5.0) * user["activity"]
    if user["goal"] == "loss":
        goal = bmr - 500.0
    elif user["goal"] == "gain":
        goal = bmr + 500.0
    else:
        goal = bmr
    return goal

def toJSON(doc):
    return json.dumps(doc, sort_keys=True)

####### Requests #########
@app.get("/user_database")
def get_users():
    user_jsonbase = user_database
    #print(user_jsonbase)
    return jsonify(user_jsonbase)

@app.put('/user_database')
def create_user():
    if request.is_json:
        nur = request.get_json()
        id , new_user = setUserProfile(nur["name"], nur["age"], nur["weight"], nur["height"], nur["goal"], nur["sex"], nur["activity"])
        user_database[id] = new_user
        with open("Databases/user_database.json", "w") as u_d:
            u_d.write(json.dumps(user_database,indent=4))
        #response = requests.put("/Databases/user_database",json=new_user.toJSON())
        return new_user, 201
    return {"TypeError:":"Request is not JSON"},415

@app.put('/update_user_database')
def update_user(): # gets user_id and parameters to be changed as request
    if request.is_json:
        req = request.get_json()
        user= user_database[str(req["user_id"])]
        print(f"------Updating {user['name']}------")
        new_user = user
        for key, value in req["parameters"].items():
            new_user[key] = value
        user_database[req["user_id"]] = new_user
        with open("Databases/user_database.json", "w") as u_d:
            u_d.write(json.dumps(user_database, indent=4))
        return new_user, 201
    return {"TypeError:": "Request is not JSON"}, 415

@app.put('/update_calories')
def add_calories():
    if request.is_json:
        req = request.get_json()
        print(f"------Adding {req['amount']} for {user_database[current_user_id]['name']}------")
        user_database[current_user_id]["kcal_intake"] += req["calories"]
        with open("Databases/user_database.json", "w") as u_d:
            u_d.write(json.dumps(user_database, indent=4))
        return user_database, 201
    return {"TypeError:": "Request is not JSON"}, 415

@app.put('/FoodData/updateDatabase')
def update_Food_Data(): # stream [dict,dict,....]
    if request.is_json:
        req = request.get_json()
        user_foodData = build_own_database(req)
        return user_foodData, 201
    return {"TypeError:": "Request is not JSON"}, 415

@app.put('/Scale/weightObject')
def update_Food_Data():
    if request.is_json:
        return  201
    return {"TypeError:": "Request is not JSON"}, 415
##### building databases ########

def build_food_database(data_path):
    print(f"------Building Database------")
    food_database = defaultdict(dict)
    tracked_nutrients = [1008,1003, 1005, 1004] # kcal,Protein, Carbohydrates,total Fat
    with open(data_path) as data:
        f = json.load(data)
        for fooditem in f["FoundationFoods"]:
            name = (fooditem["description"].split(","))[0]
            food_database[name]= {elem["nutrient"]['name']: elem["amount"] for elem in fooditem["foodNutrients"]if elem["nutrient"]['id'] in tracked_nutrients}

    with open("Databases/food_kcal_database.json", "w") as kcal_saved:
            kcal_saved.write(json.dumps(food_database,indent=4))
    return food_database

def build_own_database(fooditems:list):
    print(f"------Building favorite Database------")
    food_database = defaultdict()
    with open("Databases/user_food_database", "w") as ufd:
        while fooditems:
            new_item = fooditems.pop()
            if new_item in food_database.keys():
                for item in food_database.keys():
                    if new_item == food_database[item]:
                        food_database[item] = new_item
            else:
                food_database[len(food_database.keys()) + 1] = new_item
        ufd.write(json.dumps(food_database,indent=4))
    return food_database


###### System Settings #######
def initialize():
    if args["init"] == True:
        cal_data = build_food_database("FoodData_Central_foundation_food_json_2022-04-28.json")
    else:
        with open("Databases/food_kcal_database.json") as d:
            cal_data = json.load(d)
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
    food_database = initialize()
    current_user_id = 0
    app.run()