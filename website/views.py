# import everything needed
from flask import Blueprint, render_template, request, flash;
from flask_login import login_required, current_user;
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, NumberRange

from . import db;
from .models import User, Expense;
from datetime import datetime, timedelta;
from sqlalchemy import and_


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
    # automatically set this variable to nothing
    db_user_expenses = [None];

    if (request.method == "POST"):
        # get options from user
        form_option_date = request.form.get("date_filter");
        form_option_category = request.form.get("category_filter")
        
        # if user didn't choose options from drop-down menu's, flash message
        if (form_option_date == None and form_option_category == None):
            flash("Please choose options!", category="error");
            return render_template("overall.html", user=current_user);
    
        # if they did, get drop-down menu values from the user
        else:
            # get date values
            current_date = datetime.now();

            # week variables
            start_of_week = current_date - timedelta(days=current_date.weekday() + 1)
            end_of_week = start_of_week + timedelta(days=6)
            start_week = start_of_week.strftime("%Y-%m-%d");
            end_week = end_of_week.strftime("%Y-%m-%d");

            # month variables
            start_of_month = current_date.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            start_month = start_of_month.strftime("%Y-%m-%d");
            end_month = end_of_month.strftime("%Y-%m-%d");

            # year variables
            start_of_year = current_date.replace(month=1, day=1)
            end_of_year = current_date.replace(month=12, day=31)
            start_year = start_of_year.strftime("%Y-%m-%d");
            end_year = end_of_year.strftime("%Y-%m-%d");




            # --------------------------------------------------------
            # show expenses from all time, from all categories
            if (form_option_date == "all" and form_option_category == "all"):
                db_user_expenses = Expense.query.filter_by(user_id=current_user.id);
                return render_template("overall.html", user=current_user, expenses=db_user_expenses);
        
            # show expenses from all time, and from a specific category
            elif (form_option_date == "all" and form_option_category != "all"):
                db_user_expenses = Expense.query.filter_by(category=form_option_category, user_id=current_user.id);
                return render_template("overall.html", user=current_user, expenses=db_user_expenses);
            




            # --------------------------------------------------------
            # show expenses from the current week, from all categories
            if (form_option_date == "week" and form_option_category == "all"):
                db_user_expenses = Expense.query.filter(and_(Expense.trackDate >= start_week, Expense.trackDate <= end_week, Expense.user_id == current_user.id)).all();
                return render_template("overall.html", user=current_user, expenses=db_user_expenses);
        
            # show expenses from the current week, from a specific categories
            elif (form_option_date == "week" and form_option_category != "all"):
                db_user_expenses = Expense.query.filter(and_(Expense.category == form_option_category, Expense.trackDate >= start_week, Expense.trackDate <= end_week, Expense.user_id == current_user.id)).all();
                return render_template("overall.html", user=current_user, expenses=db_user_expenses);






            # --------------------------------------------------------
            # show expenses from the current month, from all categories
            if (form_option_date == "month" and form_option_category == "all"):
                db_user_expenses = Expense.query.filter(and_(Expense.trackDate >= start_month, Expense.trackDate <= end_month, Expense.user_id == current_user.id)).all();
                return render_template("overall.html", user=current_user, expenses=db_user_expenses);
        
            # show expenses from the current month, from a specific categories
            elif (form_option_date == "month" and form_option_category != "all"):
                db_user_expenses = Expense.query.filter(and_(Expense.category == form_option_category, Expense.trackDate >= start_month, Expense.trackDate <= end_month, Expense.user_id == current_user.id)).all();
                return render_template("overall.html", user=current_user, expenses=db_user_expenses);
            





            # --------------------------------------------------------
            # show expenses from the current year, from all categories
            if (form_option_date == "year" and form_option_category == "all"):
                db_user_expenses = Expense.query.filter(and_(Expense.trackDate >= start_year, Expense.trackDate <= end_year, Expense.user_id == current_user.id)).all();
                return render_template("overall.html", user=current_user, expenses=db_user_expenses);
        
            # show expenses from the current year, from a specific categories
            elif (form_option_date == "year" and form_option_category != "all"):
                db_user_expenses = Expense.query.filter(and_(Expense.category == form_option_category, Expense.trackDate >= start_year, Expense.trackDate <= end_year, Expense.user_id == current_user.id)).all();
                return render_template("overall.html", user=current_user, expenses=db_user_expenses);

    return render_template("overall.html", user=current_user, expenses=db_user_expenses);
