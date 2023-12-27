import uuid
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.db.base_db import get_session, Base


async def is_user_obj_owner(
    obj_model: Base, obj_id: uuid.UUID, current_user: User, session: AsyncSession = Depends(get_session)
) -> bool:
    model_task = await session.get(obj_model, obj_id)
    if model_task.author.user != current_user:
        raise HTTPException(status_code=403, detail="Can't change task, where you are not author")
    return True
