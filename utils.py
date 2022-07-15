import json
from collections import defaultdict

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

def setUserProfile(database ,name, age, weight, height, goal, sex, activity): #activity should be 1.2 , 1.5 or 1.7
    args = locals()
    new_user = {str(parameters):values for parameters, values in args.items()}
    id = len(database.keys()) + 1
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
