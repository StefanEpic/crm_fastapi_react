from src.apps.auth.models import User
from src.apps.crm.models import Department, Project, Employee, Photo, Task


async def test_model():
    department = Department(title="Model")
    project = Project(title="Model")
    user = User(email="model@model.com", password="12345")
    employee = Employee(
        family="Model", name="Model", surname="Model", phone="+4545454", department_id=department.id, user_id=user.id
    )
    photo = Photo(url="Model", path="Model", employee_id=employee.id)
    task = Task(title="Model", author_id=employee.id, projects=[project.id], employees=[employee.id])

    assert str(department) == "Model"
    assert str(project) == "Model"
    assert str(user) == "model@model.com"
    assert str(employee) == "Model M.M."
    assert str(photo) == "Model"
    assert str(task) == "Model"
