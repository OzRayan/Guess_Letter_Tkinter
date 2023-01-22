#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!

# noinspection PyProtectedMember
from peewee_validates import Validator, StringField, validate_not_empty

"""
Degree:         Faculty of Creative Arts, Technologies and Science
Department:     Computer Science and Technology
University:     University of Bedfordshire
Author:         Oszkar Feher
Date:           21 October 2022
"""


class BaseForm(Validator):
    """BaseForm class for input validation. It makes sure that input fields are not empty.
    :inherit: Validator from peewee_validates"""
    # Fields as in database, all required
    first_name = StringField(required=True, max_length=40,
                             validators=[validate_not_empty()])
    last_name = StringField(required=True, max_length=40,
                            validators=[validate_not_empty()])
    username = StringField(required=True, max_length=40,
                           validators=[validate_not_empty()])
    password = StringField(required=True, max_length=40,
                           validators=[validate_not_empty()])


class UserForm(BaseForm):
    """UserForm class for user registration input validation.
    This class use the BaseForm class
    :inherit: BaseForm
    """
    pass
