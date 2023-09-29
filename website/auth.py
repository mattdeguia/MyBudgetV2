# NOTE: this file is the "Blueprint" that holds different webpages relating to the user logging in
# NOTE: login, logout, and signup

# Import everything needed:
# Blueprint: used to create modular and reusable sets of routes and views
#            each blueprint can define its own routes, views, and templates, 
#            making it easier to structure and maintain large web applications.
# render_template: used to render template web pages
# request: used for using GET and POST requests
# flash: used to display messages to screen
# redirect/url_for: allows us to "redirect" the web user to the "url for" the homepage
from flask import Blueprint, render_template, request, flash, redirect, url_for;

# imports the User() entity from models.py
from .models import User;

# helps us hash the password and validate the hashed password
from werkzeug.security import generate_password_hash, check_password_hash;

# imports the "db" database object from "__init__.py"
from . import db;

# used for user authentication and session management
from flask_login import login_user, login_required, logout_user, current_user;


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
auth = Blueprint("auth", __name__);              # use the Blueprint() function to make this file contain some URLs inside of it
                                                 # similar to the views.py file, but this will hold different URLs inside of it



# ------------------------------------------------------------------------------
# In Flask, a "route" refers to a URL pattern that is associated with a specific view function.
# Routes define the mapping between URLs and the Python functions that should be executed when 
# a client makes an HTTP request to a particular URL
# GET - getting info from the server
# POST - sending info to the server
@auth.route("/login", methods=["GET", "POST"])                           
def login():
    # get the data from the form
    if (request.method == "POST"):
        email = request.form.get("email");
        password = request.form.get("password");
    
        # query the database
        # this is how to search for these values in the database
        # - filter all the emails by "email"
        # - only show the first value
        user = User.query.filter_by(email=email).first();
    
        # if the user exists in the database
        if (user):
            # if "user.password" and "password" are the same, keep the user logged in and redirect to home
            if (check_password_hash(user.password, password)):
                flash("Logged in successfully", category="success");                # show message
                login_user(user, remember=True);                                    # start the session for keeping user logged in
                return redirect(url_for("views.home"));                             # redirect to the home page
            else:
                flash("Incorrect email or password", category="error");
        # if user doesn't exist
        else:
            flash("User does not exist", category="error");

    # render the webpage
    return render_template("login.html", user=current_user);



# ------------------------------------------------------------------------------
@auth.route("/logout")   
# user must be logged in to log out. duhhh
@login_required                        
def logout():
    # end the session, the LoginManager() object "login_manager" we created in __init__.py keeps track of this
    logout_user();
    # after logging out, redirect user to the login() function, which takes the user to the login.html page
    return redirect(url_for("auth.login"));



# ------------------------------------------------------------------------------
@auth.route("/sign-up", methods=["GET", "POST"])                          
def sign_up():
    # process user data
    if (request.method == "POST"):
        email = request.form.get("email");
        firstName = request.form.get("firstName");
        password1 = request.form.get("password1");
        password2 = request.form.get("password2");
    
        # query the database and check if user exists in database
        user = User.query.filter_by(email=email).first();
        if (user):
            flash("User already exists", category="error");
        # if user doesn't already exist in database, validate their inputs
        elif (len(email) < 4):
            # display error message
            # the "category" will categorize the message, this is used style it
            flash("Email must be greater than 3 characters.", category="error");
        elif (len(firstName) < 2):
            flash("First name must be greater than 1 character.", category="error");
        elif (password1 != password2):
            flash("Passwords do not match.", category="error");
        elif (len(password1) < 7):
            flash("Password must be at least 7 characters.", category="error");
            pass;
        
        # if user input is valid, create user and add user to the database
        else:
            # create new user with validated user inputs
            new_user = User(email=email,
                            first_name=firstName,
                            password=generate_password_hash(password1, method="sha256"));
            
            # add and commit the user to the database
            db.session.add(new_user);
            db.session.commit();

            # remember that the user is logged in
            login_user(new_user, remember="True");

            # display message
            flash("Account created!", category="success");

            # redirect the user
            # in "views.home":
            #   the "views" is the blueprint name
            #   the "home" is the function (which contains the webpage) we use to redirect us
            return redirect(url_for("views.home"));
    
    return render_template("sign_up.html", user=current_user);

