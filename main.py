import ast, gpiozero,signal,requests, json, argparse
from collections import defaultdict
from flask import Flask, render_template, jsonify, request
from website import create_application
###### User Settings ########
try:
    with open("website/Databases/user_database.json", "r") as u_d:
        user_database = json.load(u_d)
except:
    user_database = defaultdict()

##### building databases ########



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse the arguments to setup the scale")
    parser.add_argument('--init', action="store_true" ,help="initializes the Database")
    #parser.add_argument('--flask', action="store_true")
    args = vars(parser.parse_args())

    app = create_application()
    food_database = initialize()
    current_user_id = 0
    app.run(debug=True)