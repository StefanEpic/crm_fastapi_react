import datetime
import enum
import uuid
from typing import Optional, List
from sqlalchemy import Column, ForeignKey, Table, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from src.apps.auth.models import User
from src.db.base_db import Base
from src.base_utils.base_validators import name_valid, phone_valid


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
    UniqueConstraint("task_id", "project_id", name="uix_task_project"),
)

task_employee = Table(
    "task_employee",
    Base.metadata,
    Column("task_id", ForeignKey("task.id")),
    Column("employee_id", ForeignKey("employee.id")),
    UniqueConstraint("task_id", "employee_id", name="uix_task_employee"),
)


class Department(Base):
    __tablename__ = "department"

    title: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    employees: Mapped[Optional[List["Employee"]]] = relationship(back_populates="department", lazy="selectin")

    def __str__(self):
        return self.title


class Photo(Base):
    __tablename__ = "photo"

    url: Mapped[str]
    path: Mapped[str]

    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"), index=True)
    employee: Mapped["Employee"] = relationship(back_populates="photo", single_parent=True, lazy="selectin")

    __table_args__ = (UniqueConstraint("employee_id"),)

    def __str__(self):
        return str(self.path).split("/")[-1]


class Employee(Base):
    __tablename__ = "employee"

    family: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(12), unique=True)
    photo: Mapped["Photo"] = relationship(back_populates="employee", lazy="selectin")
    my_tasks: Mapped[List["Task"]] = relationship(back_populates="author", lazy="selectin")
    tasks: Mapped[List["Task"]] = relationship(secondary=task_employee, back_populates="employees", lazy="selectin")

    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("department.id"))
    department: Mapped["Department"] = relationship(back_populates="employees", lazy="selectin")

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(single_parent=True, lazy="selectin")

    __table_args__ = (UniqueConstraint("user_id"),)

    def __str__(self) -> str:
        return f"{self.family} {self.name[0]}.{self.surname[0]}."

    @validates("family", "name", "surname")
    def validate_name(self, key, *names):
        for name in names:
            if name:
                return name_valid(name)

    @validates("phone")
    def validate_phone(self, key, phone):
        if phone:
            return phone_valid(phone)


class Project(Base):
    __tablename__ = "project"

    title: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(default="")
    is_active: Mapped[bool] = mapped_column(default=True)

    tasks: Mapped[List["Task"]] = relationship(secondary=task_project, back_populates="projects", lazy="selectin")

    def __str__(self):
        return self.title


class Task(Base):
    __tablename__ = "task"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(default="")
    status: Mapped[Optional[TaskStatus]] = mapped_column(default=TaskStatus.todo)
    priority: Mapped[Optional[TaskPriority]] = mapped_column(default=TaskPriority.none)
    start: Mapped[Optional[datetime.datetime]] = mapped_column(default=datetime.datetime.utcnow)
    end: Mapped[Optional[datetime.datetime]]
    is_active: Mapped[bool] = mapped_column(default=True)

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"))
    author: Mapped[Employee] = relationship(back_populates="my_tasks", lazy="selectin")

    projects: Mapped[List[Project]] = relationship(secondary=task_project, back_populates="tasks", lazy="selectin")
    employees: Mapped[List[Employee]] = relationship(secondary=task_employee, back_populates="tasks", lazy="selectin")

    def __str__(self):
        return self.title
