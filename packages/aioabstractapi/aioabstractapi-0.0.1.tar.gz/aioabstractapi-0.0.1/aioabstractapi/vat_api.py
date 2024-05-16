from .base import BaseClient

from .const import (
    HTTPMethods,
    Networks
)

from .models._country_vat import Country
from .models._company import Company
from .models.vat_validate import Validate
from .models.vat_category import Category
from .models.vat_calculate import Calculate

from typing import Optional

class VATValidator(BaseClient):
    """
    VAT Validator API client.
        Consists of API methods only.
        All other methods are hidden in the BaseClient.
    """

    API_DOCS = "https://docs.abstractapi.com/vat-validation"

    def __init__(self, token: str) -> None:
        """
        Init VAT Validator API client
            :param token: Your API token from https://www.abstractapi.com/
        """
        super().__init__()
        self.__token = token
        self.network = Networks.VAT

    async def validate(self, vat_number: str) -> Validate:
        """
        Use this method to check VAT validity

        Args:
            vat_number str: The VAT number to validate.

        Returns:
            Validate: Validate object            
        """
        method = HTTPMethods.GET
        url = f'{self.network}{Networks.BASE}/validate?api_key={self.__token}&vat_number={vat_number}'

        response = await self._make_request(
            method=method, url=url
        )

        data = {}

        for k,v in response.items():
            if k == "country":
                v = Country(**v)
            elif k == "company":
                v = Company(**v)
            elif k == "vat_number":
                k = 'number'
            data[k] = v

        return Validate(**data)  

    async def calculate(self, amount: float, country_code: str, is_vat_included: bool = False, vat_category: Optional[str] = None) -> Calculate:
        """
        Use this method to calculate a VAT compliant price given a country and price, as well as such optional values as the type of goods.

        Args:
            amount float: The amount that you would like to get the VAT amount for or from.
            country_code: The two letter ISO 3166-1 alpha-2 code of the country in which the transaction takes place.    
            is_vat_included: If the amount already has VAT added and you’d like to do the reverse calculation and split out the amount and VAT, set this parameter to true. If this parameter is not explicitly included it will default to false.
            vat_category: Some countries offer a reduced VAT rate for certain categories of goods. To determine if a reduced VAT is available and to apply it to the final amount, include the vat_category in the request.
        
        Returns:
            Calculate: Calculate object            
        """

        vc = ""
        if vat_category:
            vc = f"&vat_category={vat_category}"
        if is_vat_included:
            is_vat_included = "true"
        else:
            is_vat_included = "false"
        

        method = HTTPMethods.GET
        url = f'{self.network}{Networks.BASE}/calculate?api_key={self.__token}&amount={amount}&country_code={country_code}&is_vat_incl={is_vat_included}{vc}'

        response = await self._make_request(
            method=method, url=url
        )

        data = {}

        for k,v in response.items():
            if k == "country":
                v = Country(**v)
            elif k in ["vat_amount", "vat_category", "vat_rate"]:
                k: str = k.replace('vat_', '')
            data[k] = v

        return Calculate(**data) 
    
    async def get_categories(self, country_code: str) -> list[Category]:
        """
        Use this method to get the latest VAT rates, including the reduced rates for certain categories, for a specific country.

        Args:
            country_code str: The two letter ISO 3166-1 alpha-2 code of the country in which the transaction takes place.
        
            Returns:
                list[Category]: list of Category objects.
        """

        method = HTTPMethods.GET
        url = f'{self.network}{Networks.BASE}/categories?api_key={self.__token}&country_code={country_code}'

        response = await self._make_request(
            method=method, url=url
        )

        data = []
        for category in response:
            data.append(Category(**category))

        return data