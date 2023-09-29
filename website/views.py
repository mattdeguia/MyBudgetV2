# NOTE: this file is the "Blueprint" that holds different webpages relating to the general website

# a blueprint is a way to organize and structure a larger Flask application into smaller, reusable components or modules.
# blueprints allow you to define groups of related routes, view functions, templates, and static files as separate entities 
# that can be registered and integrated into your main Flask applicatio
from flask import Blueprint, render_template

# used for user authentication and session management
from flask_login import login_required, current_user;





# ------------------------------------------------------------------------------
views = Blueprint("views", __name__);               # use the Blueprint() function to make the "views" variable contain some roots/URLs inside of it
                                                    # similar to the auth.py file, but this will hold different roots/URLs inside of it


@views.route('/')                                   # this is called a "decorator", which is are usually used with functions below it
@login_required                                     # NOTE: this won't allow users to the login.html page when they're not logged in
                                                    # flask knows the user if a user is logged in based on the LoginManager() object created in __init__.py
def home():                                         # this function runs whenever we go to the root
    return render_template("home.html", user=current_user);