from pydantic import BaseModel

class Formats(BaseModel):

    international: str
    local: str
    