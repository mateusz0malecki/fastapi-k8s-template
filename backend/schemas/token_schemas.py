from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    email: EmailStr | None = None
