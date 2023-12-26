import uuid
from abc import ABC, abstractmethod
from typing import List, Dict

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def get_list(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    Base CRUD class
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
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        return res

    async def add_one(self, data: BaseModel) -> BaseModel:
        """
        Add one model exemplar
        :param data: exemplar data
        :return: exemplar data
        """
        try:
            res = self.model(**data.model_dump())
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e.orig))

    async def edit_one(self, self_id: uuid.UUID, data: BaseModel) -> BaseModel:
        """
        Edit one model exemplar
        :param self_id: uuid model exemplar
        :param data: new data
        :return: exemplar data
        """
        try:
            res = await self.session.get(self.model, self_id)
            if not res:
                raise HTTPException(status_code=404, detail="Not found")
            res_data = data.model_dump(exclude_unset=True)
            for key, value in res_data.items():
                setattr(res, key, value)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_one(self, self_id: uuid.UUID) -> Dict:
        """
        Delete one model exemplar
        :param self_id: uuid model exemplar
        :return: dictionary
        """
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        await self.session.delete(res)
        await self.session.commit()
        return {"detail": "success"}
