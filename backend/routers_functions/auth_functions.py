from fastapi import status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import timedelta

from schemas import user_schemas
from auth.jwt_helper import authenticate_user, create_token, ACCESS_TOKEN_EXPIRE_MINUTES
from exceptions.user_exceptions import CredentialsException
from db.db_models.user_models import UserModel


async def login_user(username: str, password: str, db: Session):
    user = authenticate_user(username, password, db)
    if not user:
        raise CredentialsException
    access_token = create_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token}


async def register_user(
        request: user_schemas.UserCreate,
        response: Response,
        db: Session
):
    created_user = UserModel(
        email=request.email,
        password=request.password
    )
    try:
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
        return created_user
    except IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "message": "Email is already used, try again.",
            "error": e
        }
