import string
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

    asset_id: int
    price: float
    alert_type: bool


class AlertCreate(AlertBase):
    """
    This is the model that we use when we wish to create a new alert. We expect ...
    """

    user_id: int


class Alert(IDModelMixin, DateTimeModelMixin, AlertBase):
    """
    This extends our base model to include id, created, updated
    Functionally it represents one row of the 'alerts' table.
    """

    user_id: int
    soft_delete: bool
    active: bool
    triggered: bool
    name: str
    code: str


class AlertUpdate(AlertBase):
    """
    Alert can be updated
    """

    pass
