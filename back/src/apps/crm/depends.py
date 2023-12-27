import uuid
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base_db import get_session


async def is_user_obj_owner(
    obj_model: BaseModel, obj_id: uuid.UUID, user_id: uuid.UUID, session: AsyncSession = Depends(get_session)
) -> bool:
    current_obj = await session.get(obj_model, obj_id)
    if current_obj.author_id != user_id:
        raise HTTPException(status_code=403, detail="Can't change task, where you are not author")
    return True
