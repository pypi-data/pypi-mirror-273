from pydantic import BaseModel

from ._country_vat import Country

class Calculate(BaseModel):
    """{
        "amount_excluding_vat":"175.00",
        "amount_including_vat":"208.25",
        "vat_amount":"33.25",
        "vat_category":"standard",
        "vat_rate":"0.190",
        "country":{
            "code":"DE",
            "name":"Germany"
        }
    }"""
    amount_excluding_vat: float
    amount_including_vat: float
    amount: float
    category: str
    rate: float
    country: Country