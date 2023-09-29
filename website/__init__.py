
# ------------------------------------------------------------------------------
# 1. import all necessary frameworks/extensions
from flask import Flask                         # import flask module
from flask_sqlalchemy import SQLAlchemy         # import database module
from flask_login import LoginManager;           # the "LoginManage" class helps us manage all the user login related things


# ------------------------------------------------------------------------------
# 2. create database object
db = SQLAlchemy();
DB_NAME = "database.db";



# ------------------------------------------------------------------------------
# 3. create the application
# NOTE: this code runs EVERYTIME the webpage is opened
def create_app():       
    # +++++++++++++++++++++++++++++++++++++++++++++++                                        
    # 3a. create a Flask object
    app = Flask(__name__);                                      # __name__ is automaticaly the name of the project
    app.config["SECRET_KEY"] = "123456";                        # this is the secret password for the website

    # +++++++++++++++++++++++++++++++++++++++++++++++ 
    # 3b. connect database to application
    # this is the location of our database
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}";       # this stores the database in the ~/website folder
    db.init_app(app);                                                     # initialize our database for our app

    # +++++++++++++++++++++++++++++++++++++++++++++++ 
    # 3c. Import adn register the blueprints (aka routes aka webpages) from "views.py" and "auth.py"
    # The "." in ".views" says that we are getting it from the "views.py" file that's in the same folder
    # NOTE: In Flask, a "view" refers to a Python function that handles an HTTP request and returns an HTTP response
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/");
    app.register_blueprint(auth, url_prefix="/");

    # +++++++++++++++++++++++++++++++++++++++++++++++ 
    # 3d. import the entities from "models.py"
    from .models import User, Note;

    # The app.app_context() function call creates a context manager that allows you 
    # to run code within the context of your Flask application
    with app.app_context():
        # the "create_()" examines your model classes and creates the corresponding 
        # database tables, columns, and relationships.
        db.create_all()

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # 3e. create a LoginManager() object to manage the session
    # keeps track of whether a user is logged in or not
    login_manager = LoginManager();                             # create the object
    login_manager.login_view = "auth.login";                    # redirect the user if the user is NOT logged in
    login_manager.init_app(app);                                # tell the login manager what app we're using

    # tell Flask-Login how to retrieve a user object associated with a user session
    @login_manager.user_loader
    def load_user(id):
        # we query the database to get the user's id
        return User.query.get(int(id));
    
    # +++++++++++++++++++++++++++++++++++++++++++++++
    return app;

