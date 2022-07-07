import re
from typing import Optional
from pydantic import EmailStr
from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel
from app.models.token import AccessToken

# NOTE: these are similar to CRUD -> one to Create, one to Update, one to 'find' in the database for either Read or Delete


class UserBase(CoreModel):
    """
    The base user model
    """

    email: EmailStr
    phone_number: str


class UserCreate(CoreModel):
    """
    The paramaters allowed when creating a user
    """

    email: EmailStr
    phone_number: str


class UserUpdate(CoreModel):
    """
    The paramaters allowed when updating a user
    """

    email: EmailStr
    phone_number: str


class User(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    This extends our base model to include id, created, updated
    Functionally it represents one row of the 'users' table.
    """

    pass
