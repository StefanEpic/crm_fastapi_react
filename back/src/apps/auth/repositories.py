import uuid
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.apps.auth.models import User
from src.apps.auth.schemas import UserCreate, UserUpdate, UserLogin, ReturnTokenSchema, RefreshTokenSchema
from src.apps.auth.utils import Hasher, error_401, pwd_context, create_access_jwt, create_refresh_jwt, decode_jwt
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

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
            raise HTTPException(status_code=400, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e.orig))

    async def edit_one_user(self, user_id: uuid.UUID, user: UserUpdate):
        try:
            res = await self.session.get(User, user_id)
            if not res:
                raise HTTPException(status_code=404, detail="Not found")
            res_data = user.model_dump(exclude_unset=True)
            hashed_password = Hasher.get_password_hash(res_data.pop("password"))
            res_data.update({"password": hashed_password})

            for key, value in res_data.items():
                setattr(res, key, value)

            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


class AuthRepository(UserRepository):
    async def get_access_token(self, data: UserLogin) -> ReturnTokenSchema:
        # check if email exists
        stmt = select(User).where(User.email == data.email)
        user = await self.session.execute(stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise error_401
        # check if password matches
        matches = pwd_context.verify(data.password, user.password)
        if not matches:
            raise error_401
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
            raise error_401
        if data["mode"] != "refresh_token":
            raise error_401
        # check if user exists
        stmt = select(User).where(User.email == data["email"])
        user = await self.session.execute(stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise error_401
        # generate new tokens
        data = {"email": user.email}
        access_tkn = await create_access_jwt(data)
        refresh_tkn = await create_refresh_jwt(data)
        return ReturnTokenSchema(
            email=user.email, access_token=access_tkn, refresh_token=refresh_tkn, token_type="bearer"
        )
