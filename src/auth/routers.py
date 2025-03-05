from src.auth.dependecis import AccessTokenBearer
from src.con.main import get_session
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .services import UserService
from .utils import create_access_token, verify_password

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import  JSONResponse
from datetime import timedelta


auth_router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()


REFRESH_TOKEN_EXPIRY= 30
@auth_router.post(
    "/signup",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED
)

async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):

    phone = user_data.phone

    user_exists = await user_service.user_exists(phone, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User with phone already exists",
        )

    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post('/login')
async def login_users(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    phone = login_data.phone
    password = login_data.password

    user = await user_service.get_user_by_phone(phone, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'phone': user.phone,
                    'user_id': int(user.id),
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'phone': user.phone,
                    'user_id': int(user.id),

                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message":"Login successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "phone": user.phone,
                        "id": int(user.id)
                    }
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid phone or password"
    )