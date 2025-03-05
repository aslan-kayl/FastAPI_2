from src.auth.schemas import UserCreateModel
from src.con.models import User
from src.auth.utils import generate_passwd_hash

def convert_user_create_to_orm(user_create: UserCreateModel) -> User:
    data = user_create.model_dump()
    plain_password = data.pop('password')
    data["password_hash"] = generate_passwd_hash(plain_password)
    return User(**data)