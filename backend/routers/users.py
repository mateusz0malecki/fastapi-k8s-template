from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session
from typing import Any

from schemas import user_schemas
from db.database import get_db
from auth.jwt_helper import check_if_active_user, check_if_superuser
from settings import get_settings
from routers_functions.users_functions import read_all_users_func, read_current_user_func, edit_current_user_func, \
    read_user_func, edit_user_admin_status_func, deactivate_user_func, delete_user_func

app_settings = get_settings()
router = APIRouter(prefix=f"{app_settings.root_path}", tags=["Users"])


@router.get(
    "/users",
    status_code=status.HTTP_200_OK
)
async def read_all_users(
        db: Session = Depends(get_db),
        page: int = 1,
        page_size: int = 25,
        current_user: user_schemas.UserDetail = Depends(check_if_active_user),
):
    """
    ## Get list of all users.
    Query parameters:
    - **page** - integer, default = 1
    - **page_size** - integer, default = 25

    User authentication required.
    """
    return await read_all_users_func(page, page_size, current_user, db)


@router.get(
    "/users/me",
    response_model=user_schemas.UserDetail,
    status_code=status.HTTP_200_OK
)
async def read_current_user(
        db: Session = Depends(get_db),
        current_user: user_schemas.UserDetail = Depends(check_if_active_user),
):
    """
    ## Get info about current user.
    User authentication required.
    """
    return await read_current_user_func(current_user, db)


@router.put(
    "/users/me",
    response_model=user_schemas.UserDetail | Any,
    status_code=status.HTTP_202_ACCEPTED
)
async def edit_current_user(
        response: Response,
        request: user_schemas.UserEdit,
        db: Session = Depends(get_db),
        current_user: user_schemas.UserDetail = Depends(check_if_active_user),
):
    """
    ## Edit current user.
    Body:
    - **name** - string, optional
    - **password** - string, optional
    - **repeat_password** - string, optional, must match "password" if provided

    User authentication required.
    """
    return await edit_current_user_func(response, request, current_user, db)


@router.get(
    "/users/{user_id}",
    response_model=user_schemas.UserDetail,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_if_superuser)]
)
async def read_user(
        user_id: str,
        db: Session = Depends(get_db)
):
    """
    ## Get info about user.
    Admin authentication required.
    """
    return await read_user_func(user_id, db)


@router.patch(
    "/users/{user_id}/admin",
    response_model=user_schemas.UserDetail,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(check_if_superuser)]
)
async def edit_user_admin_status(
        user_id: str,
        db: Session = Depends(get_db),
):
    """
    ## Edit user is_admin status.
    Admin authentication required.
    """
    return await edit_user_admin_status_func(user_id, db)


@router.patch(
    "/users/{user_id}/deactivate",
    response_model=user_schemas.UserDetail,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(check_if_superuser)]
)
async def deactivate_user(
        user_id: str,
        db: Session = Depends(get_db),
):
    """
    ## Deactivate user account.
    Admin authentication required.
    """
    return await deactivate_user_func(user_id, db)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_if_superuser)]
)
async def delete_user(
        user_id: str,
        db: Session = Depends(get_db),
):
    """
    ## Delete user.
    Admin authentication required.
    """
    return await delete_user_func(user_id, db)
