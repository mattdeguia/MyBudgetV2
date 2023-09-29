# the "." represents the current directory that "models.py" is in, in this case it's ~/website
from . import db;

# module that helps us log users in
from flask_login import UserMixin;

# module that helps with dates and times
from sqlalchemy.sql import func


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# define a schema for the "Note" entity
class Note(db.Model):
    # attributes for the entity
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))           # foregin key references "User" entity, must be lowercase

# define a schema for the "User" entity
# for our "User" object in particular, we want to use "UserMixin" because that module helps with user logins and stuff
class User(db.Model, UserMixin):
    # attributes for the entity
    id = db.Column(db.Integer, primary_key=True);
    email = db.Column(db.String(150), unique=True);
    password = db.Column(db.String(150));
    first_name = db.Column(db.String(150));

    # this entity is related to the "Note" entity
    notes = db.relationship('Note');                                    # this establishes a relationship to the "Notes" entity
                                                                        # this says that each user can have multiple associated notes,
                                                                        # this is a one-to-many relationship