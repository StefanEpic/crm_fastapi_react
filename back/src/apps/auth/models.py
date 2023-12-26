import datetime
import enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates
from src.db.db import Base
from src.utils.validators import email_valid


class UserPermission(enum.Enum):
    admin = "Администратор"
    moderator = "Модератор"
    user = "Пользователь"
    none = "Нет прав"


class User(Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    registration_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    permission: Mapped[UserPermission] = mapped_column(default=UserPermission.none)

    def __str__(self):
        return self.email

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)
