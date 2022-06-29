from typing import Optional
from pydantic import EmailStr, constr
from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel
from app.models.token import AccessToken

# NOTE: these are similar to CRUD -> one to Create, one to Update, one to 'find' in the database for either Read or Delete


class UserBase(CoreModel):
    """
    The base user model. We don't include those things that are in the database we don't want exposed as any model that extends this will have and have access to its values.
    """

    email: EmailStr
    phone_number: str


class UserCreate(CoreModel):
    """
    This is the model that we use when we wish to create a new user. We expect email and password.
    email
    password
    """

    email: EmailStr
    phone_number: str


class UserUpdate(CoreModel):
    """
    Users can update their details
    """

    email: EmailStr
    phone_number: str


class User(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    This extends our base model to include id, created, updated and salt.
    Functionally it represents one row of the 'users' table.
    """

    pass

class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Public model. This is what we return to a request. Optionally includes access_token and profile details.
    """

    # we're deciding what we send out publicly here --> UserBase + mixins

    # + extra fields ( authorisation)
    access_token: Optional[AccessToken]