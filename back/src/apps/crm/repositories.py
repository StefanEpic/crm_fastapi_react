import os
import uuid
from typing import List, Union, Dict
from fastapi import File, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DBAPIError
from config import MEDIA_URL, BASE_SITE_URL
from src.apps.auth.models import User, UserPermission
from src.apps.crm.models import Department, Photo, Employee, Project, Task, task_project, task_employee
from src.apps.crm.schemas import EmployeeRead, EmployeeReadWithTasks, MyEmployeeUpdate
from src.base_utils.base_errors import ERROR_404
from src.base_utils.base_repository import SQLAlchemyRepository, RepositoryWithoutInactive, get_obj_by_params


class DepartmentRepository(SQLAlchemyRepository):
    model = Department


class ProjectRepository(SQLAlchemyRepository, RepositoryWithoutInactive):
    model = Project


class TaskRepository(SQLAlchemyRepository, RepositoryWithoutInactive):
    model = Task

    async def add_one_task(self, data: BaseModel, author_id: uuid.UUID = None):
        try:
            # Workaround for solve bag sqlalchemy "object don't have _sa_instance_state"
            task = self.model(**data.model_dump(exclude=["projects", "employees"]))
            if author_id:
                employee = await get_obj_by_params(Employee, {"user_id": author_id}, self.session)
                task.author_id = employee.id
            self.session.add(task)
            await self.session.commit()

            for project_id in data.projects:
                project = await get_obj_by_params(Project, {"id": project_id}, self.session)
                project_res = task_project.insert().values(task_id=task.id, project_id=project.id)
                await self.session.execute(project_res)
            for employee_id in data.employees:
                employee = await get_obj_by_params(Employee, {"id": employee_id}, self.session)
                employee_res = task_employee.insert().values(task_id=task.id, employee_id=employee.id)
                await self.session.execute(employee_res)

            await self.session.commit()
            await self.session.refresh(task)
            return task
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e.orig).split(":")[-1].replace("\n", "").strip())
        except DBAPIError as e:
            raise HTTPException(status_code=400, detail=str(e.orig).split(":")[-1].replace("\n", "").strip())

    async def edit_one_task(self, self_id: uuid.UUID, data: BaseModel, author_id: uuid.UUID = None):
        try:
            # Workaround for solve bag sqlalchemy "object don't have _sa_instance_state"
            task = await get_obj_by_params(Task, {"id": self_id}, self.session)
            employee = await get_obj_by_params(Employee, {"user_id": author_id}, self.session)
            if task.author_id != employee.id:
                if (
                    employee.user.permission != UserPermission.moderator
                    and employee.user.permission != UserPermission.admin
                ):
                    raise HTTPException(status_code=403, detail="Can't change task, where you are not author")

            task_res = data.model_dump(exclude_unset=True, exclude=["projects", "employees"])
            for key, value in task_res.items():
                setattr(task, key, value)
            self.session.add(task)
            await self.session.commit()

            if data.projects:
                task.projects = []
                for project_id in data.projects:
                    project = await get_obj_by_params(Project, {"id": project_id}, self.session)
                    project_res = task_project.insert().values(task_id=task.id, project_id=project.id)
                    await self.session.execute(project_res)
            if data.employees:
                task.employees = []
                for employee_id in data.employees:
                    employee = await get_obj_by_params(Employee, {"id": employee_id}, self.session)
                    employee_res = task_employee.insert().values(task_id=task.id, employee_id=employee.id)
                    await self.session.execute(employee_res)

            await self.session.commit()
            await self.session.refresh(task)
            return task
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e.orig).split(":")[-1].replace("\n", "").strip())

    async def deactivate_one_task_my(self, self_id: uuid.UUID, author_id: uuid.UUID) -> Dict:
        stmt = select(Task).join(Employee, Task.author_id == Employee.id).where(Employee.user_id == author_id)
        task = await self.session.execute(stmt)
        task = task.scalar_one_or_none()
        if not task:
            raise ERROR_404
        return await super().deactivate_one(self_id)


class EmployeeRepository(SQLAlchemyRepository):
    model = Employee

    async def get_list_employees(self, offset: int, limit: int) -> List[EmployeeRead]:
        """
        Get list of the employee exemplars
        :param offset: offset value
        :param limit: limit value
        :return: list model exemplars
        """
        stmt = (
            select(self.model)
            .join(User, self.model.user_id == User.id)
            .where(User.is_active.is_(True), User.is_verify.is_(True))
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def get_one_employee(self, self_id: uuid.UUID) -> Union[EmployeeReadWithTasks, None]:
        """
        Get one employee exemplar
        :param self_id: uuid of the exemplar
        :return: model exemplar
        """
        stmt = (
            select(self.model)
            .join(User, self.model.user_id == User.id)
            .where(self.model.id == self_id, User.is_active.is_(True), User.is_verify.is_(True))
        )
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if not res:
            raise ERROR_404
        return res

    async def get_one_employee_me(self, user_id: uuid.UUID) -> Union[EmployeeReadWithTasks, None]:
        """
        Get one my employee exemplar
        :param user_id: user uuid
        :return: model exemplar
        """
        return await get_obj_by_params(Employee, {"user_id": user_id}, self.session)

    async def edit_one_employee_me(
        self, user_id: uuid.UUID, data: MyEmployeeUpdate
    ) -> Union[EmployeeReadWithTasks, None]:
        """
        Edit one my employee exemplar
        :param user_id: user uuid
        :param data: new data
        :return: model exemplar
        """
        employee = await get_obj_by_params(Employee, {"user_id": user_id}, self.session)
        return await super().edit_one(employee.id, data)

    async def deactivate_one_employee(self, employee_id: uuid.UUID) -> dict:
        """
        Deactivate one employee exemplar
        :param employee_id: uuid model exemplar
        :return: dictionary
        """
        stmt = select(User).join(Employee, User.id == Employee.user_id).where(Employee.id == employee_id)
        user = await self.session.execute(stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise ERROR_404
        user.is_active = False
        self.session.add(user)
        await self.session.commit()
        return {"detail": "success"}


class PhotoRepository(SQLAlchemyRepository, RepositoryWithoutInactive):
    model = Photo

    async def __put_photo(self, user_id: uuid.UUID, image: File):
        employee = await get_obj_by_params(Employee, {"user_id": user_id}, self.session)

        stmt = select(Photo).where(Photo.employee_id == employee.id)
        old_photo = await self.session.execute(stmt)
        old_photo = old_photo.scalar_one_or_none()
        if old_photo:
            os.remove(old_photo.path)
            await self.session.delete(old_photo)
            await self.session.commit()

        try:
            contents = await image.read()
            filepath = f"{MEDIA_URL}/{employee.user.email}.{str(image.filename).split('.')[-1]}"
            url = BASE_SITE_URL + "/media/" + image.filename
            res = Photo(url=url, path=filepath, employee_id=employee.id)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)

            with open(filepath, "wb") as f:
                f.write(contents)
            return res
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig).split(":")[-1].replace("\n", "").strip()
            )

    async def __delete_photo(self, photo: Photo) -> dict:
        os.remove(photo.path)
        await self.session.delete(photo)
        await self.session.commit()
        return {"detail": "success"}

    async def put_one_photo(self, employee_id: uuid.UUID, image: File):
        employee = await get_obj_by_params(Employee, {"id": employee_id}, self.session)
        return await self.__put_photo(employee.user_id, image)

    async def put_one_photo_my(self, user_id: uuid.UUID, image: File):
        return await self.__put_photo(user_id, image)

    async def delete_one_photo(self, photo_id: uuid.UUID):
        photo = await get_obj_by_params(self.model, {"id": photo_id}, self.session)
        if not photo:
            raise ERROR_404
        return await self.__delete_photo(photo)

    async def delete_one_photo_my(self, user_id: uuid.UUID):
        stmt = (
            select(self.model)
            .join(Employee, self.model.employee_id == Employee.id)
            .join(User, User.id == Employee.user_id)
            .where(User.id == user_id)
        )
        photo = await self.session.execute(stmt)
        photo = photo.scalar_one_or_none()
        if not photo:
            raise ERROR_404
        return await self.__delete_photo(photo)
