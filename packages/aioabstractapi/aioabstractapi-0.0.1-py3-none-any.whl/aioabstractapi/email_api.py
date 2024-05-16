from .base import BaseClient

from .const import (
    HTTPMethods,
    Networks
)

from .models.email import Email

class EmailValidator(BaseClient):
    """
    Email Validator API client.
        Consists of API methods only.
        All other methods are hidden in the BaseClient.
    """

    API_DOCS = "http://docs.abstractapi.com/email-validation"

    def __init__(self, token: str) -> None:
        """
        Init Email Validator API client
            :param token: Your API token from https://www.abstractapi.com/
        """
        super().__init__()
        self.__token = token
        self.network = Networks.EMAIL

    async def validate(self, email: str, auto_correct: bool = False) -> Email:
        """
        Use this method to check Email validity

        Args:
            email str: The email address to validate.
            auto_correct bool: You can chose to disable auto correct. To do so, just input false for the auto_correct param. By default, auto_correct is turned on.

        Returns:
            Email: Email object            
        """
        method = HTTPMethods.GET
        url = f"{self.network}{Networks.BASE}?api_key={self.__token}&email={email}&auto_correct={auto_correct}"

        response = await self._make_request(
            method=method, url=url
        )
        
        data = {}

        for k,v in response.items():
            if k in ['is_valid_format', 'is_free_email', 'is_disposable_email', 'is_role_email', 'is_catchall_email', 'is_mx_found', 'is_smtp_valid']:
                v = v['value']
                if k in ['is_free_email', 'is_disposable_email', 'is_role_email', 'is_catchall_email']:
                    k = k.replace('_email', '')
            elif k == 'autocorrect':
                k = "auto_correct"
            data[k] = v

        return Email(**data)