from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from typing import Any

from schemas import token_schemas, user_schemas
from db.database import get_db
from routers_functions.auth_functions import login_user, register_user
from settings import get_settings

app_settings = get_settings()
router = APIRouter(prefix=f"{app_settings.root_path}", tags=["Auth"])


@router.post(
    '/login',
    response_model=token_schemas.Token
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
    ## Login with email and password.
    FormData:
    - **username**: string, required
    - **password**: string, required
    """
    return await login_user(form_data.username, form_data.password, db)


@router.post(
    "/register",
    response_model=user_schemas.UserDetail | Any,
    status_code=status.HTTP_201_CREATED
)
async def register(
        response: Response,
        request: user_schemas.UserCreate,
        db: Session = Depends(get_db),
):
    """
    ## Create new user.
    Body:
    - **email**: string, required, unique
    - **password**: string, required to be at least 8 characters long and contain at least 1 letter and 1 number
    - **repeat_password**: string, required to match password
    """
    return await register_user(request, response, db)
