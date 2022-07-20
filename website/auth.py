from flask import jsonify,Blueprint, render_template, request,flash
import json
from utils import setUserProfile, build_own_database
from . import user_db as db

auth = Blueprint('auth',__name__)

with open("website/Databases/user_database.json", "r") as u_d:
    user_database = json.load(u_d)
auth.route('/update_calories', methods=['POST'])

@auth.get("/user_database")
def get_users():
    user_jsonbase = user_database
    #print(user_jsonbase)
    return jsonify(user_jsonbase)

@auth.put('/user_database')
def create_user():
    if request.is_json:
        nur = request.get_json()
        id , new_user = setUserProfile(nur["name"], nur["age"], nur["weight"], nur["height"], nur["goal"], nur["sex"], nur["activity"])
        user_database[id] = new_user
        with open("website/Databases/user_database.json", "w") as u_d:
            u_d.write(json.dumps(user_database,indent=4))
        #response = requests.put("/Databases/user_database",json=new_user.toJSON())
        return new_user, 201
    return {"TypeError:":"Request is not JSON"},415

@auth.put('/update_user_database')
def update_user(): # gets user_id and parameters to be changed as request
    if request.is_json:
        req = request.get_json()
        user= user_database[str(req["user_id"])]
        flash(f"------Updating {user['name']}------",category='success')
        new_user = user
        for key, value in req["parameters"].items():
            new_user[key] = value
        user_database[req["user_id"]] = new_user
        with open("Databases/user_database.json", "w") as u_d:
            u_d.write(json.dumps(user_database, indent=4))
        return new_user, 201
    return {"TypeError:": "Request is not JSON"}, 415

@auth.post('/update_calories')
def add_calories():
    if request.is_json:
        req = request.get_json()
        flash(f"------Adding {req['amount']} for {user_database[0]['name']}------",category='success')
        user_database[0]["kcal_intake"] += req["calories"]
        with open("Databases/user_database.json", "w") as u_d:
            u_d.write(json.dumps(user_database, indent=4))
        return user_database, 201
    return {"TypeError:": "Request is not JSON"}, 415

@auth.put('/FoodData/updateDatabase')
def update_Food_Data(): # stream [dict,dict,....]
    if request.is_json:
        req = request.get_json()
        user_foodData = build_own_database(req)
        return user_foodData, 201
    return {"TypeError:": "Request is not JSON"}, 415

@auth.get('/Scale/weightObject')
def scaleFoodItem():
    if request.is_json:
        #weight = 234.0 TODO get the weight signal
        req = request.get_json()
        weight = req['weight']
        weight_metric = weight // 100.0
        weighted_nutrients= {x: y*weight_metric for x,y in (db.request["name"].lower()).items()}
        user_database[0]["kcal_intake"] = weighted_nutrients["Energy"]
        return jsonify(weighted_nutrients), 201
    return {"TypeError:": "Request is not JSON"}, 415
