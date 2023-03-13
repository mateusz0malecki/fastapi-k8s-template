from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta, datetime

from schemas import token_schemas
from db.database import get_db
from db.db_models.user_models import UserModel
from auth.hash import Hash
from exceptions.user_exceptions import CredentialsException
from settings import get_settings
from schemas import user_schemas


app_settings = get_settings()
SECRET_KEY = app_settings.jwt_secret
ALGORITHM = app_settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(app_settings.access_token_expire_minutes)

router = APIRouter(tags=["Auth"])
auth_scheme = OAuth2PasswordBearer(tokenUrl='login')


def authenticate_user(
        email: str,
        password: str,
        db: Session = Depends(get_db)
) -> UserModel | bool:
    user = UserModel.get_user_by_email(db=db, email=email)
    if not user:
        return False
    if not Hash.verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user


def create_token(data: dict, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
        token: str = Depends(auth_scheme),
        db: Session = Depends(get_db)
) -> UserModel:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise CredentialsException
        token_data = token_schemas.TokenData(email=email)
    except JWTError:
        raise CredentialsException
    user = UserModel.get_user_by_email(db=db, email=token_data.email)
    if not user:
        raise CredentialsException
    return user


def check_if_active_user(current_user: user_schemas.UserDetail = Depends(get_current_user)):
    if not current_user.is_active:
        raise CredentialsException
    return current_user


def check_if_superuser(current_user: user_schemas.UserDetail = Depends(get_current_user)):
    if not current_user.is_admin:
        raise CredentialsException
    return current_user
