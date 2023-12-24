import datetime
import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.apps.base import Base
from src.utils.validators import email_valid


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    registration_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.email

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)
