import datetime
import enum
import uuid
from typing import Optional, List
from sqlalchemy import Column, ForeignKey, Table, String, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from src.apps.auth.models import User
from src.db.base_db import Base
from src.utils.validators import name_valid


class TaskStatus(enum.Enum):
    todo = "Запланировано"
    doing = "В работе"
    done = "На проверке"
    release = "Завершено"


class TaskPriority(enum.Enum):
    height = "Высокий приоритет"
    normal = "Средний приоритет"
    low = "Низкий приоритет"
    none = "Приоритет не указан"


task_project = Table(
    "task_project",
    Base.metadata,
    Column("task_id", ForeignKey("task.id")),
    Column("project_id", ForeignKey("project.id")),
)

task_employee = Table(
    "task_employee",
    Base.metadata,
    Column("task_id", ForeignKey("task.id")),
    Column("employee_id", ForeignKey("employee.id")),
)


class Department(Base):
    __tablename__ = "department"

    title: Mapped[str] = mapped_column(String(100), unique=True)
    employees: Mapped[Optional[List["Employee"]]] = relationship(back_populates="department")

    def __str__(self):
        return self.title


class Photo(Base):
    __tablename__ = "photo"

    url: Mapped[str]
    path: Mapped[str]

    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"))
    employee: Mapped["Employee"] = relationship(back_populates="photo", single_parent=True, lazy="selectin")

    __table_args__ = (UniqueConstraint("employee_id"),)

    def __str__(self):
        return self.employee.email


class Employee(Base):
    __tablename__ = "employee"

    last_name: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    second_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(12), unique=True)
    photo: Mapped["Photo"] = relationship(back_populates="employee")
    my_tasks: Mapped[Optional[List["Task"]]] = relationship(back_populates="author")
    tasks: Mapped[Optional[List["Task"]]] = relationship(
        secondary=task_employee, back_populates="employees", lazy="selectin"
    )

    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("department.id"))
    department: Mapped["Department"] = relationship(back_populates="employees")

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(single_parent=True, lazy="selectin")

    __table_args__ = (UniqueConstraint("user_id"),)

    def __str__(self) -> str:
        return str(self.user.email)

    @validates("first_name", "second_name", "last_name")
    def validate_name(self, key, *names):
        for name in names:
            if name:
                return name_valid(name)


class Project(Base):
    __tablename__ = "project"

    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text(1000), nullable=False, default="")
    is_active: Mapped[bool] = mapped_column(default=True)

    tasks: Mapped[Optional[List["Task"]]] = relationship(
        secondary=task_project, back_populates="projects", lazy="selectin"
    )

    def __str__(self):
        return self.title


class Task(Base):
    __tablename__ = "task"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text(1000), nullable=False, default="")
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.todo)
    priority: Mapped[TaskPriority] = mapped_column(default=TaskPriority.none)
    start: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    end: Mapped[datetime.datetime]
    is_active: Mapped[bool] = mapped_column(default=True)

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"))
    author: Mapped["Employee"] = relationship(back_populates="tasks")

    projects: Mapped[List["Project"]] = relationship(secondary=task_project, back_populates="tasks", lazy="selectin")

    employees: Mapped[List["Employee"]] = relationship(secondary=task_employee, back_populates="tasks", lazy="selectin")

    def __str__(self):
        return self.title
