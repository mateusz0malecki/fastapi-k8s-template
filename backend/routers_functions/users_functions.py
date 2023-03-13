from fastapi import status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import parse_obj_as

from schemas import user_schemas
from db.db_models.user_models import UserModel
from exceptions.user_exceptions import UserNotFound


async def read_all_users_func(
        page: int,
        page_size: int,
        current_user: user_schemas.UserDetail,
        db: Session
):
    users = UserModel.get_all_users(db) if current_user.is_admin else UserModel.get_all_active_users(db)
    first = (page - 1) * page_size
    last = first + page_size
    users_model = parse_obj_as(list[user_schemas.UserBase], users)
    response = user_schemas.UserPagination(
        users_model,
        "/api/v1/users",
        first,
        last,
        page,
        page_size
    )
    return response


async def read_current_user_func(
        current_user: user_schemas.UserDetail,
        db: Session
):
    user = UserModel.get_user_by_email(db, current_user.email)
    if not user:
        raise UserNotFound(str(current_user.user_id))
    return user


async def edit_current_user_func(
        response: Response,
        request: user_schemas.UserEdit,
        current_user: user_schemas.UserDetail,
        db: Session
):
    user_to_edit = UserModel.get_user_by_email(db, current_user.email)
    if not user_to_edit:
        raise UserNotFound(str(current_user.user_id))
    if request.email:
        user_to_edit.email = request.email
    if request.password:
        user_to_edit.password = request.password
    try:
        db.commit()
        db.refresh(user_to_edit)
        return user_to_edit
    except IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "message": "Email is already used, try again.",
            "error": e
        }


async def read_user_func(
        user_id: str,
        db: Session
):
    user = UserModel.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


async def edit_user_admin_status_func(
        user_id: str,
        db: Session
):
    user = UserModel.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise UserNotFound(user_id)
    user.is_admin = False if user.is_admin else True
    db.commit()
    db.refresh(user)
    return user


async def deactivate_user_func(
        user_id: str,
        db: Session
):
    user = UserModel.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise UserNotFound(user_id)
    user.email = ""
    user.password = ""
    user.is_active = False
    user.is_admin = False
    db.commit()
    db.refresh(user)
    return user


async def delete_user_func(
        user_id: str,
        db: Session
):
    user = UserModel.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise UserNotFound(user_id)
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
