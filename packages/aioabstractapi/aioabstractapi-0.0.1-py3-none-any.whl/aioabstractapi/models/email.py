from pydantic import BaseModel

class Email(BaseModel):

    email: str
    auto_correct: str
    deliverability: str
    quality_score: float
    is_valid_format: bool
    is_free: bool
    is_disposable: bool
    is_role: bool
    is_catchall: bool
    is_mx_found: bool
    is_smtp_valid: bool
    