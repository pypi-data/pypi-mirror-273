from .base import BaseClient

from .const import (
    HTTPMethods,
    Networks
)

from .models.iban import Iban

class IBANValidator(BaseClient):
    """
    IBAN Validator API client.
        Consists of api methods only.
        All other methods are hidden in the BaseClient.
    """

    API_DOCS = "https://docs.abstractapi.com/iban-validation"

    def __init__(self, token: str) -> None:
        """
        Init IBAN Validator API client
            :param token: Your API token from https://www.abstractapi.com/
        """
        super().__init__()

        self.__token = token
        self.network = Networks.IBAN

    async def validate(self, iban: str) -> Iban:
        """
        Use this method to check IBAN validity
        
        Args:
            iban str: The IBAN to validate. Note that the API will accept white spaces, so BE71 0961 2345 6769 is considered as valid as BE71096123456769.
        
        Returns:
            Iban: Iban object    
        """

        method = HTTPMethods.GET
        url = f"{self.network}{Networks.BASE}?api_key={self.__token}&iban={iban}"

        response = await self._make_request(
            method=method, url=url
        )

        return Iban(**response)