import json
from collections import defaultdict
from website.models import User
def build_own_database(fooditems:list):
    print(f"------Building favorite Database------")
    food_database = defaultdict()
    with open("website/Databases/user_food_database", "w") as ufd:
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

def setUserProfile(name, age, weight, height, goal, sex, activity): #activity should be 1.2 , 1.5 or 1.7
    args = locals()
    cal_intake = set_calorie_goal(sex,height,age,activity,weight)
    new_user = User(name=name,age=age,weight=weight, height=height,
                    goal=goal,sex=sex,activity=activity,kcal_intake=cal_intake,current_intake=0)
    return new_user

def set_calorie_goal(sex,height,age,activity, weight):
    if sex == "female":
        bmr = ((weight * 10.0 + height) * 6.25 - age * 5.0 - 161.0) * activity
    else:
        bmr = ((weight * 10.0 + height) * 6.25 - age * 5.0 + 5.0) * activity
    if "goal" == "loss":
        bmr = bmr - 500.0
    elif "goal" == "gain":
        bmr = bmr + 500.0
    return bmr

def toJSON(doc):
    return json.dumps(doc, sort_keys=True)
