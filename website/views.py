# import everything needed
from flask import Blueprint, render_template, request, flash;
from flask_login import login_required, current_user;
from . import db;
from .models import User, Expense;
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, NumberRange

# store blueprints of this file into the "views" object
# this object is used in other files to access different URLs
views = Blueprint("views", __name__);               


# ------------------------------------------------------------------------------
# takes user to the home page
@views.route('/')                               
def home():
    # *****NOTE: the "user" in the return statement refers to the "User" class in "models.py"                                         
    return render_template("home.html", user=current_user);



# ------------------------------------------------------------------------------
# handles HTTP POST requests in the daily page
@views.route('/daily', methods=["GET", "POST"])
@login_required
def daily():
    if (request.method == "POST"):
        # get values from the form
        form_money_spent = int(request.form.get("money"));
        form_category = request.form.get("category");

        # validate money
        if (form_money_spent <= 0):
            flash("Please enter an amount greater than 0", category="error");
            return render_template("daily.html", user=current_user);

        # query these inputs to the database
        # NOTE: to access values from the current user: current_user.id, current_user.email, etc...
        # NOTE: while creating a new expense, notice that we only give price/category/user_id. the trackDate gets filled in automatically
        new_expense = Expense(price=form_money_spent, category=form_category, user_id=current_user.id);
        db.session.add(new_expense);
        db.session.commit();
        flash("New expense added!", category="success");

    return render_template("daily.html", user=current_user);



# ------------------------------------------------------------------------------
# handles HTTP GET requests in the overall page
@views.route('/overall', methods=["GET", "POST"])
@login_required
def overall():
    # query all expenses from the user that's logged in
    db_user_expenses = Expense.query.filter_by(user_id=current_user.id);
    return render_template("overall.html", user=current_user, expenses=db_user_expenses);


# ------------------------------------------------------------------------------
# handles HTTP GET requests in the category page
@views.route('/cat')
@login_required
def cat():
    return render_template("cat.html", user=current_user);
