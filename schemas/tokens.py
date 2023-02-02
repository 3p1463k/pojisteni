from sqlmodel import SQLModel


class Token(SQLModel):

    """Token base model"""

    access_token: str
    token_type: str
