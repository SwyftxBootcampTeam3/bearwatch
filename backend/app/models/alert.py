from typing import Optional
from pydantic import EmailStr, constr
from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel
from app.models.user import User
from app.models.asset import Asset

# NOTE: these are similar to CRUD -> one to Create, one to Update, one to 'find' in the database for either Read or Delete


class AlertBase(CoreModel):
    """
    The base alert model. We don't include those things that are in the database we don't want exposed as any model that extends this will have and have access to its values.
    """

    user_id: str
    asset_id: str
    price: int
    alert_type: bool
    soft_delete: bool



class AlertCreate(CoreModel):
    """
    This is the model that we use when we wish to create a new alert. We expect ...
    """

    user_id: str
    asset_id: str
    price: int
    alert_type: bool


class AlertUpdate(CoreModel):
    """
    Alert can be updated
    """

    price: int


class Alert(IDModelMixin, DateTimeModelMixin, AlertBase):
    """
    This extends our base model to include id, created, updated and salt.
    Functionally it represents one row of the 'users' table.
    """

    pass