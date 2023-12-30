import uuid
from typing import List, Union

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.apps.auth.models import User
from src.apps.auth.schemas import UserCreate, UserUpdate, ReturnTokenSchema, RefreshTokenSchema, UserRead
from src.apps.auth.utils import Hasher, pwd_context, create_access_jwt, create_refresh_jwt, decode_jwt
from src.base_utils.base_errors import ERROR_401, ERROR_404
from src.base_utils.base_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_list_users(self, offset: int, limit: int) -> List[UserRead]:
        """
        Get list of the user exemplars
        :param offset: offset value
        :param limit: limit value
        :return: list model exemplars
        """
        stmt = (
            select(self.model)
            .where(self.model.is_active.is_(True), self.model.is_verify.is_(True))
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def get_one_user(self, self_id: uuid.UUID) -> Union[UserRead, None]:
        """
        Get one user exemplar
        :param self_id: uuid of the exemplar
        :return: model exemplar
        """
        res = await self.session.get(self.model, self_id)
        if not res or not res.is_active or not res.is_verify:
            raise ERROR_404
        return res

    async def add_one_user(self, user: UserCreate):
        try:
            hashed_password = Hasher.get_password_hash(user.password)
            new_user = User(
                email=user.email,
                password=hashed_password,
            )
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))

    async def edit_one_user(self, user_id: uuid.UUID, user: UserUpdate):
        try:
            res = await self.session.get(User, user_id)
            if not res:
                raise ERROR_404
            res_data = user.model_dump(exclude_unset=True)
            if "password" in res_data.keys():
                hashed_password = Hasher.get_password_hash(res_data.pop("password"))
                res_data.update({"password": hashed_password})

            for key, value in res_data.items():
                setattr(res, key, value)

            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class AuthRepository(UserRepository):
    async def get_access_token(self, data: UserCreate) -> ReturnTokenSchema:
        # check if email exists
        stmt = select(User).where(
            User.email == data.email, User.is_active.is_(True), User.is_verify.is_(True), User.permission != "none"
        )
        user = await self.session.execute(stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise ERROR_401
        # check if password matches
        matches = pwd_context.verify(data.password, user.password)
        if not matches:
            raise ERROR_401
        # create jwt tokens
        data = {"email": user.email}
        access_tkn = await create_access_jwt(data)
        refresh_tkn = await create_refresh_jwt(data)
        return ReturnTokenSchema(
            email=user.email, access_token=access_tkn, refresh_token=refresh_tkn, token_type="bearer"
        )

    async def get_refresh_token(self, token: RefreshTokenSchema) -> ReturnTokenSchema:
        data = await decode_jwt(token.refresh_token)
        # check if "mode": "refresh_token"
        if "email" not in data and "mode" not in data:
            raise ERROR_401
        if data["mode"] != "refresh_token":
            raise ERROR_401
        # check if user exists
        stmt = select(User).where(
            User.email == data["email"], User.is_active.is_(True), -User.is_verify.is_(True), User.permission != "none"
        )
        user = await self.session.execute(stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise ERROR_401
        # generate new tokens
        data = {"email": user.email}
        access_tkn = await create_access_jwt(data)
        refresh_tkn = await create_refresh_jwt(data)
        return ReturnTokenSchema(
            email=user.email, access_token=access_tkn, refresh_token=refresh_tkn, token_type="bearer"
        )
