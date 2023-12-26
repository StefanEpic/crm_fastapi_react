from src.apps.crm.models import Department, Photo, Employee, Project, Task
from src.utils.repository import SQLAlchemyRepository


class DepartmentRepository(SQLAlchemyRepository):
    model = Department


class PhotoRepository(SQLAlchemyRepository):
    model = Photo


class EmployeeRepository(SQLAlchemyRepository):
    model = Employee


class ProjectRepository(SQLAlchemyRepository):
    model = Project


class TaskRepository(SQLAlchemyRepository):
    model = Task
