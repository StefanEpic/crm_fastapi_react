import os
import uuid
from typing import List, Union
from fastapi import File, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from config import MEDIA_URL, BASE_SITE_URL
from src.apps.auth.models import User
from src.apps.crm.models import Department, Photo, Employee, Project, Task
from src.apps.crm.schemas import EmployeeRead, EmployeeReadWithTasks
from src.utils.base_errors import ERROR_404
from src.utils.repository import SQLAlchemyRepository


class DepartmentRepository(SQLAlchemyRepository):
    model = Department


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

    async def deactivate_one_employee(self, self_id: uuid.UUID) -> dict:
        """
        Deactivate one employee exemplar
        :param self_id: uuid model exemplar
        :return: dictionary
        """
        res = await self.session.get(self.model, self_id)
        if not res:
            raise ERROR_404
        user = await self.session.get(User, res.user_id)
        user.is_active = False
        self.session.add(user)
        await self.session.commit()
        return {"detail": "success"}


class ProjectRepository(SQLAlchemyRepository):
    model = Project


class TaskRepository(SQLAlchemyRepository):
    model = Task


class PhotoRepository(SQLAlchemyRepository):
    model = Photo

    async def put_one_photo(self, employee_id: uuid.UUID, image: File):
        employee = await self.session.get(Employee, employee_id)
        if not employee:
            raise ERROR_404

        stmt = select(Photo).where(Photo.employee_id == employee_id)
        old_photo = await self.session.execute(stmt)
        old_photo = old_photo.scalar_one_or_none()
        if old_photo:
            os.remove(old_photo.path)
            await self.session.delete(old_photo)
            await self.session.commit()

        try:
            contents = await image.read()
            filepath = f"{MEDIA_URL}/{image.filename}"
            url = BASE_SITE_URL + "/media/" + image.filename
            res = Photo(url=url, path=filepath, employee_id=employee_id)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)

            with open(filepath, "wb") as f:
                f.write(contents)
            return res
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))

    async def delete_one_photo(self, self_id: uuid.UUID):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise ERROR_404
        os.remove(res.path)
        await self.session.delete(res)
        await self.session.commit()
        return {"detail": "success"}
