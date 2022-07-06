import string
from typing import Optional
from pydantic import EmailStr, constr
from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel
from app.models.user import User
from app.models.asset import Asset

# NOTE: these are similar to CRUD -> one to Create, one to Update, one to 'find' in the database for either Read or Delete


class AlertBase(CoreModel):
    """
    The base alert model
    """

    asset_id: int
    price: float
    alert_type: bool


class AlertCreate(AlertBase):
    """
    The paramaters allowed when creating an alert
    """

    user_id: int


class Alert(IDModelMixin, DateTimeModelMixin, AlertBase):
    """
    This extends our base model to include id, created, updated
    Functionally it represents one row of the 'alerts' table.
    It also includes asset info, which is joined from the assets table at query time
    """

    user_id: int
    soft_delete: bool
    active: bool
    triggered: bool
    asset_name: str
    asset_code: str
    asset_price: int


class AlertUpdate(CoreModel):
    """
    The paramaters allowed when updating an alert
    """

    price: float
    alert_type: bool
