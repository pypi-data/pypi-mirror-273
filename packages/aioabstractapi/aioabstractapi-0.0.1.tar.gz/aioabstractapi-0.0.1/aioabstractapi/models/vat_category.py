from pydantic import BaseModel

class Category(BaseModel):

    country_code: str
    rate: float
    category: str
    description: str