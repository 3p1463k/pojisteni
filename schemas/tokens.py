from pydantic import BaseModel


class Token(BaseModel):

    """Token base model"""

    access_token: str
    token_type: str
