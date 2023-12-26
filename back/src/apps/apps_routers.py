from src.apps.auth.routers.auth import router as router_auth_auth
from src.apps.auth.routers.users import router as router_auth_user

from src.apps.crm.routers.departments import router as router_crm_department
from src.apps.crm.routers.employees import router as router_crm_employee
from src.apps.crm.routers.photos import router as router_crm_photo
from src.apps.crm.routers.projects import router as router_crm_project
from src.apps.crm.routers.tasks import router as router_crm_task

apps_routers = [
    router_auth_auth,
    router_auth_user,
    router_crm_department,
    router_crm_employee,
    router_crm_photo,
    router_crm_project,
    router_crm_task,
]
