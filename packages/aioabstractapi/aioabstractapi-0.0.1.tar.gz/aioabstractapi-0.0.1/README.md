# abstractapi.com asynchronous api wrapper

**Docs**: https://docs.abstractapi.com

**Install**
``` bash
pip install aioabstractapi
```

**Basic usage**
``` python
from aioabstractapi import (
    EmailValidator, PhoneValidator,
    IBANValidator, VATValidator)

#email validation
email_validator = EmailValidator(token="12345...")
email = await email_validator.validate(
    email = "example@example.site"
)
print(email.email)


#phone validation
phone_validator = PhoneValidator(token="12345...")
phone = await phone_validator.validate(
    phone = "+x(xxx)xxx-xx-xx"
)
print(phone.valid)


#IBAN validation
iban_validator = IBANValidator(token="12345...")
iban = await iban_validator.validate(
    iban = "BE71096*****6769"
)
print(iban.valid)


#VAT validation
vat_validator = VATValidator(token="12345...")
#Use this method to check VAT validity
vat = await vat_validator.validate( 
    vat_number = "SE55*****88001"
)
print(vat.company)

#Use this method to calculate a VAT compliant price.
calcs = await vat_validator.calculate(
    amount = 100,
    country_code = "DE"
)
print(calcs.rate)

#Use this method to get the latest VAT rates
categories = await vat_validator.get_categories(
    country_code = "DE"
)
print(categories.description)


#close connection
await email_validator.close()
...
await vat_validator.close()

```