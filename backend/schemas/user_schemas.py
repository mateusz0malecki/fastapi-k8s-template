import re
from pydantic import EmailStr, validator, root_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

from auth.hash import Hash
from .helpers import BaseConfig, CustomPagination


class UserBase(BaseConfig):
    user_id: UUID
    email: EmailStr
    is_admin: bool
    is_active: bool


class UserDetail(UserBase):
    email: str
    updated_at: Optional[datetime]
    created_at: Optional[datetime]


class UserPasswords(BaseConfig):
    password: Optional[str]
    repeat_password: Optional[str]

    @root_validator(pre=True)
    def verify_password_match(cls, values):
        password = values.get("password")
        repeat_password = values.get("repeatPassword")
        if password != repeat_password:
            raise ValueError("Two given passwords do not match.")
        return values

    @validator('password')
    def validate_password(cls, v):
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        if not pattern.match(v):
            raise ValueError(
                "Password has to be at least 8 characters long and contain at least 1 letter and 1 number."
            )
        return Hash.get_password_hash(v)


class UserCreate(UserPasswords):
    email: EmailStr
    password: str
    repeat_password: str


class UserEdit(UserPasswords):
    email: Optional[EmailStr]


class UserPagination(CustomPagination):
    records: list[UserBase] = []
