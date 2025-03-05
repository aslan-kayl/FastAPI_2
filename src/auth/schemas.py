from pydantic import BaseModel, Field, validator, field_validator
from typing import List

from sqlalchemy.sql.coercions import expect


class AdminCreateModel(BaseModel):
    username: str
    password: str

class AdminModel(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    password_hash: str = Field(exclude=True)
    is_verified: bool



class UserModel(BaseModel):
    username: str
    phone: str
    first_name: str
    last_name: str
    password_hash: str = Field(exclude=True)
    is_verified: bool


class PasswordChange(BaseModel):
    pass

class PasswordReset(BaseModel):
    pass


class EmailModel(BaseModel):
    addresses : List[str]


class UserLoginModel(BaseModel):
    phone: str = Field(..., max_length=20)
    password: str = Field(max_length=15)

import phonenumbers
from pydantic import BaseModel, Field, field_validator


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    phone: str
    password: str = Field(max_length=16)

    @field_validator("phone")
    @classmethod
    def validate_and_format_phone(cls, value: str) -> str:

        try:
            parsed = phonenumbers.parse(value, None)
        except phonenumbers.NumberParseException:
            try:
                parsed = phonenumbers.parse(value, "UZ")
            except phonenumbers.NumberParseException as e:
                raise ValueError("Incorrect format number") from e

        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Incorrect phone number")

        formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        digits = ''.join(filter(str.isdigit, formatted))
        if not (10 <= len(digits) <= 15):
            raise ValueError("Invalid phone number)")

        return formatted
