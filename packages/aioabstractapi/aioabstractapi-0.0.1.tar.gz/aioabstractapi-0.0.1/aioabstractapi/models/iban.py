from pydantic import BaseModel

class Iban(BaseModel):

    iban: str
    is_valid: bool