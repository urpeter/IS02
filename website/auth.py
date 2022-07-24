from flask import jsonify, Blueprint, render_template, request, flash, url_for
import json
from werkzeug.utils import redirect
from utils import setUserProfile, build_own_database
from . import user_db as db
from flask_login import current_user, login_user, logout_user
from .models import User, Food
from random import randrange

auth = Blueprint('auth', __name__)
with open("website/Databases/user_database.json", "r") as u_d:
    user_database = json.load(u_d)
auth.route('/update_calories', methods=['POST'])


@auth.get("/user_database")
def get_users():
    user_jsonbase = user_database

    return jsonify(user_jsonbase)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        password = request.form.get('password')
        user = User.query.filter_by(name=firstname).first()
        if user:
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.get('/sign_up')
def display_sign_up():
    return render_template('sign_up.html', user=current_user)


@auth.post('/sign_up')
def create_user():
    email = request.form.get('email')
    first_name = request.form.get('firstName')
    age = float(request.form.get('age'))
    sex = request.form.get('sex')
    goal = request.form.get('goal')
    height = float(request.form.get('height'))
    weight = float(request.form.get('weight'))
    activity = 1.5
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    new_user = setUserProfile(first_name, age, weight, height, goal, sex, activity, password1)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)
    flash('Account created!', category='success')
    return redirect(url_for('views.home'))
    # response = requests.put("/Databases/user_database",json=new_user.toJSON())


@auth.put('/update_user_database')
def update_user():  # gets user_id and parameters to be changed as request
    if request.is_json:
        req = request.get_json()
        user = user_database[str(req["user_id"])]
        flash(f"------Updating {user['name']}------", category='success')
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
    current_user.current_intake += request.form.get("calories")
    return redirect(url_for('views.home'))



