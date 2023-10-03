# import everything needed
from . import db;
from flask_login import UserMixin;
from sqlalchemy.sql import func
from datetime import date;


# define a schema for our "Expense" entity
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True);
    price = db.Column(db.Integer);
    category = db.Column(db.String(150));                                      
    trackDate = db.Column(db.Date, default=date.today());  # year-month-day 
                                                           # 2023-09-30
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"));           

    
# define a schema for the "User" entity
# we want to use "UserMixin" because that module helps with user logins and stuff
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True);
    email = db.Column(db.String(150), unique=True);
    password = db.Column(db.String(150));
    first_name = db.Column(db.String(150));
    expenses = db.relationship('Expense');                              # this establishes a one-to-many relationship to "Expense"
