# Import everything needed:
from flask import Blueprint, render_template, request, flash, redirect, url_for;
from werkzeug.security import generate_password_hash, check_password_hash;
from flask_login import login_user, login_required, logout_user, current_user;

from .models import User;
from . import db;

# store blueprints of this file into the "auth" object
# this object is used in other files to access different URLs
auth = Blueprint("auth", __name__);

# ------------------------------------------------------------------------------
# handles the HTTP POST request for logs in
@auth.route("/login", methods=["GET", "POST"])                           
def login():
    if (request.method == "POST"):
        form_email = request.form.get("email");
        form_password = request.form.get("password");

        # check if user email exists in database
        user = User.query.filter_by(email=form_email).first();

        # if email exists is in database, validate their password, then them in/redirect to home page
        if (user):
            if (check_password_hash(user.password, form_password)):
                login_user(user, remember=True);
                return redirect(url_for("views.home"));
            else:
                flash("Incorrect email or password", category="error");
        else:
            flash("User does not exist", category="error");
    
    # display the "login.html" webpage, keep the current user's data
    return render_template("login.html", user=current_user);



# ------------------------------------------------------------------------------
# logs out the user and redirects them to the home page
@auth.route("/logout")   
@login_required                     
def logout():
    logout_user();
    return redirect(url_for("views.home"));



# ------------------------------------------------------------------------------
# handles the HTTP POST request for when user signs up
@auth.route("/sign_up", methods=["GET", "POST"])                          
def sign_up():
    if (request.method == "POST"):
        form_email = request.form.get("email");
        form_firstName = request.form.get("firstName");
        form_password1 = request.form.get("password1");
        form_password2 = request.form.get("password2");
    
        # query the database and check if user exists in database
        user = User.query.filter_by(email=form_email).first();
        if (user):
            flash("User already exists", category="error");
        
        # if user doesn't already exist in database, validate their inputs
        elif (len(form_email) < 4):
            flash("Email must be greater than 3 characters.", category="error");
        elif (len(form_firstName) < 2):
            flash("First name must be greater than 1 character.", category="error");
        elif (form_password1 != form_password2):
            flash("Passwords do not match.", category="error");
        elif (len(form_password1) < 7):
            flash("Password must be at least 7 characters.", category="error");
        
        # if all user input is valid, create user/ add user to the database
        else:
            # create new user
            new_user = User(email=form_email,
                            first_name=form_firstName,
                            password=generate_password_hash(form_password1, method="sha256"));
            
            # add/commit the user to the database
            db.session.add(new_user);
            db.session.commit();

            # remember that the user is logged in
            login_user(new_user, remember="True");

            # display message and redirect to home page
            flash("Account created!", category="success");
            return redirect(url_for("views.home"));
    
    return render_template("sign_up.html", user=current_user);
