from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, user_or_email: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id / email '{user_or_email}' not found."
        )


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
            headers={"WWW-Authenticate": "Bearer"}
        )
