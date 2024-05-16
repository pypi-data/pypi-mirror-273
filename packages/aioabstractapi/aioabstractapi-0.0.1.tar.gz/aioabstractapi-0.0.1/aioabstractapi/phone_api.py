from .base import BaseClient

from .const import (
    HTTPMethods,
    Networks
)

from .models.phone import Phone
from .models._phone_formats import Formats
from .models._country import Country

from typing import Optional

class PhoneValidator(BaseClient):
    """
    Phone Validator API client.
        Consists of API methods only.
        All other methods are hidden in the BaseClient.
    """

    API_DOCS = "http://docs.abstractapi.com/phone-validation"

    def __init__(self, token: str) -> None:
        super().__init__()
        """
        Init Phone Validator API client
            :param token: Your API token from https://www.abstractapi.com/
        """
        self.__token = token
        self.network = Networks.PHONE

    async def validate(self, phone: str, country: Optional[str] = None) -> Phone:
        """
        Use this method to check Phone validity

        Args:
            phone str: The phone number to validate and verify.
            country Union[str,None]: The country’s ISO code. Add this parameter to indicate the phone number’s country, and the API will append the corresponding country code to its analysis. For instance, add country=US to indicate that the phone number is from the United States.

        Returns:
            Phonr: Phone object            
        """
        country_str = ""
        if country:
            country_str = f"&country={country}"

        method = HTTPMethods.GET
        url = f"{self.network}{Networks.BASE}?api_key={self.__token}&phone={phone}{country_str}"

        response = await self._make_request(
            method=method, url=url
        )

        data = {}

        for k, v in response.items():
            if k == "format":
                v = Formats(**v)
            elif k == "country": 
                v = Country(**v)
            data[k] = v

        return Phone(**data) #type: ignore