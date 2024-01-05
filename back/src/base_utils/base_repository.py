import uuid
from typing import List, Dict, Union
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.base_utils.base_errors import ERROR_404
from src.db.base_db import Base


async def get_obj_by_params(model: Base, filter_params: dict, session: AsyncSession) -> Union[BaseModel, None]:
    """
    Get model exemplar by user id
    :param model: ORM model
    :param filter_params: params for filter model
    :param session: async session
    :return: model exemplar
    """
    stmt = select(model).filter_by(**filter_params)
    res = await session.execute(stmt)
    res = res.scalar_one_or_none()
    if not res:
        raise ERROR_404
    return res


class BaseCRUDRepository:
    """
    Base CRUD repository
    """

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, offset: int, limit: int) -> List[BaseModel]:
        """
        Get list of the model exemplars
        :param offset: offset value
        :param limit: limit value
        :return: list model exemplars
        """
        stmt = select(self.model).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def get_one(self, self_id: uuid.UUID) -> BaseModel:
        """
        Get one model exemplar
        :param self_id: uuid of the exemplar
        :return: model exemplar
        """
        return await get_obj_by_params(self.model, {"id": self_id}, self.session)

    async def add_one(self, data: BaseModel, user_id: uuid.UUID = None) -> BaseModel:
        """
        Add one model exemplar
        :param data: exemplar data
        :param user_id: optional param if need create model exemplar for current user
        :return: exemplar data
        """
        try:
            data = data.model_dump()
            if user_id:
                data["user_id"] = user_id
            res = self.model(**data)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str(e.orig).split(':')[-1].replace('\n', '').strip())

    async def edit_one(self, self_id: uuid.UUID, data: BaseModel) -> BaseModel:
        """
        Edit one model exemplar
        :param self_id: uuid model exemplar
        :param data: new data
        :return: exemplar data
        """
        try:
            res = await get_obj_by_params(self.model, {"id": self_id}, self.session)
            res_data = data.model_dump(exclude_unset=True)
            for key, value in res_data.items():
                setattr(res, key, value)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def delete_one(self, self_id: uuid.UUID) -> Dict:
        """
        Delete one model exemplar
        :param self_id: uuid model exemplar
        :return: dictionary
        """
        res = await get_obj_by_params(self.model, {"id": self_id}, self.session)
        await self.session.delete(res)
        await self.session.commit()
        return {"detail": "success"}


class SQLAlchemyRepository(BaseCRUDRepository):
    """
    Base CRUD repository with PUT method
    """

    async def put_one(self, self_id: uuid.UUID, data: BaseModel) -> BaseModel:
        """
        Put one model exemplar
        :param self_id: uuid model exemplar
        :param data: new data
        :return: exemplar data
        """
        res = await self.session.get(self.model, self_id)
        if not res:
            return await super().add_one(data)
        else:
            return await super().edit_one(self_id, data)


class RepositoryWithoutInactive:
    """
    Repository for work with models with is_active field
    """

    model = None
    session = None

    async def get_list_without_inactive(self, offset: int, limit: int) -> List[BaseModel]:
        """
        Get list of the model exemplars without inactive
        :param offset: offset value
        :param limit: limit value
        :return: list model exemplars
        """
        stmt = select(self.model).where(self.model.is_active.is_(True)).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def get_one_without_inactive(self, self_id: uuid.UUID) -> BaseModel:
        """
        Get one model exemplar without inactive
        :param self_id: uuid of the exemplar
        :return: model exemplar
        """
        return await get_obj_by_params(self.model, {"id": self_id, "is_active": True}, self.session)

    async def deactivate_one(self, self_id: uuid.UUID) -> Dict:
        """
        Deactivate one model exemplar
        :param self_id: uuid model exemplar
        :return: dictionary
        """
        res = await get_obj_by_params(self.model, {"id": self_id}, self.session)
        res.is_active = False
        self.session.add(res)
        await self.session.commit()
        return {"detail": "success"}
