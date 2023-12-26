import datetime
import uuid
from typing import Optional, List
from pydantic import BaseModel
from src.apps.auth.schemas import UserRead
from src.apps.crm.models import TaskStatus, TaskPriority


class PhotoCreate(BaseModel):
    url: str
    employee_id: uuid.UUID


class PhotoRead(PhotoCreate):
    id: uuid.UUID
    path: str


class PhotoUpdate(BaseModel):
    url: Optional[str] = None
    employee_id: Optional[uuid.UUID] = None


class EmployeeCreate(BaseModel):
    last_name: str
    first_name: str
    second_name: str
    phone: str
    department_id: uuid.UUID
    user_id: uuid.UUID


class EmployeeRead(EmployeeCreate):
    id: uuid.UUID


class EmployeeUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    phone: Optional[str] = None
    photo: Optional[PhotoCreate] = None
    department_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None


class DepartmentCreate(BaseModel):
    title: str


class DepartmentRead(DepartmentCreate):
    id: uuid.UUID


class DepartmentUpdate(BaseModel):
    title: Optional[str] = None


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str]


class ProjectRead(ProjectCreate):
    id: uuid.UUID
    is_active: bool


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    start: datetime.datetime
    end: datetime.datetime
    projects: List[uuid.UUID]
    employees: List[uuid.UUID]


class TaskRead(TaskCreate):
    id: uuid.UUID
    is_active: bool
    author: uuid.UUID


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]
    start: Optional[datetime.datetime]
    end: Optional[datetime.datetime]
    projects: Optional[List[uuid.UUID]]
    employees: Optional[List[uuid.UUID]]


class TaskReadWithProjectsAndEmployees(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    start: datetime.datetime
    end: datetime.datetime
    is_active: bool
    author: EmployeeRead
    projects: List[EmployeeRead]
    employees: List[EmployeeRead]


class DepartmentReadWithEmployees(DepartmentCreate):
    id: uuid.UUID
    employees: Optional[List[EmployeeRead]]


class EmployeeReadWithTasks(BaseModel):
    id: uuid.UUID
    user: UserRead
    last_name: str
    first_name: str
    second_name: str
    phone: str
    department: DepartmentRead
    my_tasks: Optional[List[TaskRead]]
    tasks: Optional[List[TaskRead]]


class ProjectReadWithTasks(ProjectRead):
    tasks: TaskRead
