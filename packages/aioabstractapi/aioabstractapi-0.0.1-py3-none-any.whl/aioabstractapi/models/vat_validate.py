from pydantic import BaseModel

from ._country_vat import Country
from ._company import Company

class Validate(BaseModel):
    """{
        "vat_number":"SE556656688001",
        "valid":true,
        "company":{
            "name":"GOOGLE SWEDEN AB",
            "address":"GOOGLE IRLAND LTD \\nM COLLINS, GORDON HOUSE \\nBARROW STREET, DUBLIN 4 \\nIRLAND"
        },
        "country":{
            "code":"SE",
            "name":"Sweden"
        }
    }"""
    number: str
    valid: bool
    company: Company
    country: Country
