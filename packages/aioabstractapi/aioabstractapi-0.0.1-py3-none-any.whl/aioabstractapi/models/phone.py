from pydantic import BaseModel

from ._phone_formats import Formats
from ._country import Country

class Phone(BaseModel):

    phone: str
    valid: bool
    format: Formats
    country: Country
    location: str
    type: str
    carrier: str