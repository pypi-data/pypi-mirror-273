from strenum import StrEnum

class HTTPMethods(StrEnum):
    """Available HTTP methods."""

    GET = "GET"

class Networks(StrEnum):
    """Abstract Networks"""

    BASE = ".abstractapi.com/v1"
    EMAIL = "https://emailvalidation"
    PHONE = "https://phonevalidation" 
    IBAN = "https://ibanvalidation"
    VAT = "https://vat"