from typing import Optional
from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel

# NOTE: these are similar to CRUD -> one to Create, one to Update, one to 'find' in the database for either Read or Delete


class AssetBase(CoreModel):
    """
    The base user model. We don't include those things that are in the database we don't want exposed as any model that extends this will have and have access to its values.
    """

    name: str
    code: str
    price: float


class AssetCreate(AssetBase):
    """
    This is the model that we use when we wish to create a new asset.
    """

    pass


class Asset(IDModelMixin, DateTimeModelMixin, AssetBase):
    """
    Public model. This is what we return to a request. Optionally includes access_token and profile details.
    """

    pass
