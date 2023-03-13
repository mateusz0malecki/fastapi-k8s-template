import uuid
from sqlalchemy import String, DateTime, Boolean, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from db.database import Base


class UserModel(Base):
    __tablename__ = "user"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f'id: {self.user_id}, email: {self.email}'

    @staticmethod
    def get_all_users(db: Session):
        return db.query(UserModel).all()

    @staticmethod
    def get_all_active_users(db: Session):
        return db.query(UserModel).filter(UserModel.is_active).all()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(UserModel).filter(UserModel.is_active).filter(UserModel.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        try:
            uuid_user = uuid.UUID(user_id, version=4)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user id, try again."
            )
        if str(uuid_user) == user_id:
            return db.query(UserModel).filter(UserModel.user_id == user_id).first()
