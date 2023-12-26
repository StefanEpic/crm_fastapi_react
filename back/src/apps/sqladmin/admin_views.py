from sqladmin import ModelView

from src.apps.auth.models import User
from src.apps.crm.models import Department, Photo, Employee, Project, Task


class UserAdmin(ModelView, model=User):
    column_list = "__all__"
    form_columns = "__all__"
    # form_excluded_columns = [Category.products]
    column_details_list = "__all__"
    # name_plural = "Categories"
    can_export = False


class DepartmentAdmin(ModelView, model=Department):
    column_list = "__all__"
    form_columns = "__all__"
    # form_excluded_columns = [Category.products]
    column_details_list = "__all__"
    # name_plural = "Categories"
    can_export = False


class PhotoAdmin(ModelView, model=Photo):
    column_list = "__all__"
    form_columns = "__all__"
    # form_excluded_columns = [Category.products]
    column_details_list = "__all__"
    # name_plural = "Categories"
    can_export = False


class EmployeeAdmin(ModelView, model=Employee):
    column_list = "__all__"
    form_columns = "__all__"
    # form_excluded_columns = [Category.products]
    column_details_list = "__all__"
    # name_plural = "Categories"
    can_export = False


class ProjectAdmin(ModelView, model=Project):
    column_list = "__all__"
    form_columns = "__all__"
    # form_excluded_columns = [Category.products]
    column_details_list = "__all__"
    # name_plural = "Categories"
    can_export = False


class TaskAdmin(ModelView, model=Task):
    column_list = "__all__"
    form_columns = "__all__"
    # form_excluded_columns = [Category.products]
    column_details_list = "__all__"
    # name_plural = "Categories"
    can_export = False
