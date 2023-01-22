#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!
# for adding current time to a game record
import datetime

# ORM for Models and database connectivity
from peewee import *
# for password hashing
from werkzeug.security import generate_password_hash

"""
Degree:         Faculty of Creative Arts, Technologies and Science
Department:     Computer Science and Technology
University:     University of Bedfordshire
Author:         Oszkar Feher
Date:           21 October 2022
"""

# the created database
db = SqliteDatabase('record.db')


class BaseModel(Model):
    """BaseModel class to utilize database <db> by giving the Meta data.
    :inherit: - Model from peewee."""
    class Meta:
        database = db


class Abstract(BaseModel):
    """
    Abstract model class. A base class for all models with base fields.
    All fields are mandatory.
    :inherit: - BaseModel.
    """
    first_name = CharField(null=False, max_length=40)
    last_name = CharField(null=False, max_length=40)
    # unique - makes sure that repeated user names are not accepted
    username = CharField(null=False, unique=True, max_length=40)
    password = CharField(null=False, max_length=40)
    # unique - makes sure that repeated emails are not accepted
    joined_at = DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    # Option for further development
    is_admin = BooleanField(default=False)


class User(Abstract):
    """
    User model with additional field to register game played.
    :inherit: - Abstract.
    :methods: - create_user class method.
    """
    games = IntegerField(default=0)

    # noinspection PyShadowingNames
    @classmethod
    def create_user(cls, first_name, last_name, username,
                    password, admin=False):
        """
        Creates a customer/user.
        :param first_name: - string.
        :param last_name: - string.
        :param username: - string, must be unique.
        :param password: - string, password is saved as a hashed string not the actual password.
        :param admin: - boolean, user not admin so it's false.
        :return: - string if user already exists with same username or email.
        """
        try:
            # Makes sure that all fields are given and than it can save it.
            # If input fields are just half given, entry will not be saved and protects the database from
            # incomplete input.
            with db.transaction():
                cls.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError:
            return "User already exists!"


class GameRecord(BaseModel):
    """Game record model for saving game records.
    :inherit: BaseModel()
    """
    user_id = ForeignKeyField(User)
    level = CharField(max_length=10)
    solved = BooleanField(default=False)
    guesses = IntegerField()
    misses = IntegerField()
    timestamp = DateField(default=datetime.datetime.now)


def user(username):
    """Return a user by username"""
    return User().select().where(User.username == username)


def create_record(user_id, level, solved, guesses, misses):
    """Creates a game record."""
    if level == 3:
        text = 'Hard'
    elif level == 2:
        text = 'Medium'
    else:
        text = 'Easy'
    GameRecord.create(user_id=user_id, level=text, solved=solved, guesses=guesses, misses=misses)


def select_all_records():
    """Selects all Game records in a descending order."""
    return GameRecord.select().order_by(GameRecord.misses.desc())


# Connects to the database
db.connect()
# Creates tables, if exists don't take action
db.create_tables([GameRecord, User], safe=True)
# Closing database connection
db.close()
