from pydantic import BaseModel

from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, validator


class CoreModel(BaseModel):
    """
    Common logic for all models. ALL. <-- ALL models.
    """

    pass


class IDModelMixin(BaseModel):
    """
    This is a mixin, we don't need to define this again and again for every model that has an ID. Instead we just use this as a mixin.
    It's similar to inheritance but is more like 'functionality by composition of parts'.
    """

    id: int


class DateTimeModelMixin(BaseModel):
    """
    This is a datetime mixin. It essentially exists for when we want our returned model to have created + updated at times. We primarily include it into our 'InDB' models rather than our externally returned models.
    """

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, val: datetime) -> datetime:
        """
        this is a pydantic thing, basically it takes this class (cls) and then attempts to validate for the created_at and updated_at using the default_datetime function.
        Functionally this either returns the val if it exists else returns now
        """
        return val or datetime.now()