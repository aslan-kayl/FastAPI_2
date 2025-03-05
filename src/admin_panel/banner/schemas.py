import re

from pydantic import BaseModel, Field, constr, field_validator
from datetime import datetime
from typing import Optional
#
# BASE64_IMAGE_REGEX = re.compile(r"^data:image\/[a-zA-Z]+;base64,[A-Za-z0-9+/=]+$")
#

class Banner(BaseModel):
    id: Optional[int] = None
    title: str
    image: constr(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_main: Optional[bool] = False

    # @field_validator("image")
    # @classmethod
    # def validate_image(cls, value):
    #     if not BASE64_IMAGE_REGEX.match(value):
    #         raise ValueError("image должно быть в формате Base64 (data:image/...)")
    #     return value


class CreateBanner(BaseModel):
    title: str
    image: str
