from random import randrange
import json
from flask import Blueprint, render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Food
from . import user_db as db
from werkzeug.utils import redirect

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.post('/')
def add_calories():
    updated_user = User.query.filter_by(id=current_user.id).first()
    updated_user.current_intake += float(request.form.get("calories"))
    db.session.add(updated_user)
    db.session.commit()
    return redirect(url_for('views.home'))


@views.route('/scale_food', methods=['GET', 'POST'])
def scale():
    if request.method == 'POST':

        new_food = Food(name=request.form.get("name"),
                        Protein=request.form.get("protein"),
                        Fat=request.form.get("fat"),
                        Carbohydrate=request.form.get("carbohydrates"),
                        Energy=request.form.get("energy"),
                        user_id=current_user.id)
        print(new_food.name)
        db.session.add(new_food)
        db.session.commit()
    return render_template('scale_food.html', user=current_user)


@views.post('/scale')
def scaleFoodItem():
    randval = randrange(0, 9, 1)
    weightlists = [184.0, 237.0, 129.0, 291.0, 323.0, 336.0, 371.0, 589.0, 796, 743]
    weight = float(weightlists[randval])  # remove after testing
    req = json.loads(request.data)
    foodid = req["foodId"]
    food = Food.query.filter_by(id=foodid).first()
    foodnutrients = {"Protein": float(food.Protein)/100.0*weight,
                     "Fat": float(food.Fat)/100.0*weight,
                     "Carbohydrate": float(food.Carbohydrate)/100.0*weight,
                     "Energy": float(food.Energy)/100.0*weight}

    # weight_metric = weight // 100.0
    new_intake = current_user.current_intake + foodnutrients["Energy"]
    updated_user = User.query.filter_by(id=current_user.id).first()
    updated_user.current_intake = new_intake
    db.session.add(updated_user)
    db.session.commit()

    return jsonify({})

