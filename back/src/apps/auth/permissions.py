from typing import Annotated
from fastapi import Depends, HTTPException, status
from src.apps.auth.models import User, UserPermission
from src.apps.auth.utils import verified_user


async def check_active_user(user: User) -> User:
    if user.is_active is False or user.is_verify is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return user


async def check_permission_user(current_user: Annotated[User, Depends(verified_user)]):
    current_user = await check_active_user(current_user)
    if current_user.permission != UserPermission.none:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Don't have permissions")


async def check_permission_moderator(current_user: Annotated[User, Depends(verified_user)]):
    current_user = await check_active_user(current_user)
    if current_user.permission == UserPermission.moderator or current_user.permission == UserPermission.admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Don't have permissions")
