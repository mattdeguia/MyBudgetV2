# 1. import all necessary frameworks/extensions
from flask import Flask                         # import flask module
from flask_login import LoginManager;           # the "LoginManage" class helps us manage all the user login related thing
from flask_sqlalchemy import SQLAlchemy         # import database module



# ------------------------------------------------------------------------------
# 2. create database object
db = SQLAlchemy();
#DB_NAME = "database.db";

# ------------------------------------------------------------------------------
# 3. create the application
# NOTE: this code runs EVERYTIME the webpage is opened
def create_app():       
    # +++++++++++++++++++++++++++++++++++++++++++++++                                        
    # 3a. create a Flask object
    app = Flask(__name__);                                          # __name__ is automaticaly the name of the project
    app.config["SECRET_KEY"] = "123456";                            # this is the secret password for the website


    # +++++++++++++++++++++++++++++++++++++++++++++++ 
    # 3b. connect database to application
    # this is the location of our database

    # Old Local Database:
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}";       # create a sqlite database and store it in the ~/website folder

    # New Remote Database connection to heroku:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgres://gufuuhkjwbflau:daa84cc9b91b9043e5ee1daef0eb8c93214d6202410e0dbf3012b5348c6340ac@ec2-35-169-9-79.compute-1.amazonaws.com:5432/dddh1g8c82na2p"; 
    
    # initialize our database for our app
    db.init_app(app);                                                    




    # +++++++++++++++++++++++++++++++++++++++++++++++ 
    # 3c. Import and register the blueprints (routes/views) from "views.py" and "auth.py"
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/");
    app.register_blueprint(auth, url_prefix="/");






    # +++++++++++++++++++++++++++++++++++++++++++++++ 
    # 3d. import the database schema from "models.py"
    from .models import User, Expense;

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

