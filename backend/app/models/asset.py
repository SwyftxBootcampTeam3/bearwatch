from typing import Optional
from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel

# NOTE: these are similar to CRUD -> one to Create, one to Update, one to 'find' in the database for either Read or Delete


class AssetBase(CoreModel):
    """
    The base asset model
    """

    name: str
    code: str
    price: float


class AssetCreate(AssetBase):
    """
    The paramaters allowed when creating an asset
    """

    pass


class Asset(IDModelMixin, DateTimeModelMixin, AssetBase):
    """
    This extends our base model to include id, created, updated
    Functionally it represents one row of the 'assets' table.
    """

    pass
