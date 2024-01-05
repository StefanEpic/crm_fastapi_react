import datetime
from typing import Optional, List
from pydantic import BaseModel
from src.apps.auth.schemas import UserRead
from src.apps.crm.models import TaskStatus, TaskPriority
from pydantic import UUID4


class PhotoCreate(BaseModel):
    url: str
    employee_id: UUID4


class PhotoRead(PhotoCreate):
    id: UUID4
    path: str


class PhotoUpdate(BaseModel):
    url: Optional[str] = None
    employee_id: Optional[UUID4] = None


class MyEmployeeCreate(BaseModel):
    family: str
    name: str
    surname: str
    phone: str
    department_id: UUID4


class MyEmployeeUpdate(BaseModel):
    family: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[UUID4] = None


class EmployeeCreate(MyEmployeeCreate):
    user_id: UUID4


class EmployeeRead(EmployeeCreate):
    id: UUID4


class EmployeeUpdate(BaseModel):
    family: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    photo: Optional[PhotoCreate] = None
    department_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None


class DepartmentCreate(BaseModel):
    title: str


class DepartmentRead(DepartmentCreate):
    id: UUID4


class DepartmentUpdate(BaseModel):
    title: Optional[str] = None


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ProjectRead(ProjectCreate):
    id: UUID4
    is_active: bool


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class MyTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    projects: List[UUID4]
    employees: List[UUID4]


class MyTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    projects: Optional[List[UUID4]] = None
    employees: Optional[List[UUID4]] = None


class TaskCreate(MyTaskCreate):
    author_id: UUID4


class TaskRead(TaskCreate):
    id: UUID4
    is_active: bool
    projects: List[ProjectRead]
    employees: List[EmployeeRead]


class TaskUpdate(MyTaskUpdate):
    author_id: Optional[UUID4]


class TaskReadWithProjectsAndEmployees(BaseModel):
    id: UUID4
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    is_active: bool
    author: EmployeeRead
    projects: List[EmployeeRead]
    employees: List[EmployeeRead]


class DepartmentReadWithEmployees(DepartmentCreate):
    id: UUID4
    employees: Optional[List[EmployeeRead]] = None


class EmployeeReadWithTasks(BaseModel):
    id: UUID4
    family: str
    name: str
    surname: str
    phone: str
    user: UserRead
    photo: Optional[PhotoRead] = None
    department: Optional[DepartmentRead] = None
    my_tasks: Optional[List[TaskRead]] = None
    tasks: Optional[List[TaskRead]] = None


class ProjectReadWithTasks(ProjectRead):
    tasks: Optional[List[TaskRead]] = None
