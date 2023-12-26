from typing import Annotated
from fastapi import Depends, HTTPException
from src.apps.auth.models import User, UserPermission
from src.apps.auth.utils import verified_user


async def check_permission_user(current_user: Annotated[User, Depends(verified_user)]):
    if current_user.permission != UserPermission.none:
        return current_user
    raise HTTPException(status_code=403, detail="Don't have permissions")


async def check_permission_moderator(current_user: Annotated[User, Depends(verified_user)]):
    if current_user.permission == UserPermission.moderator or current_user.permission == UserPermission.admin:
        return current_user
    raise HTTPException(status_code=403, detail="Don't have permissions")
