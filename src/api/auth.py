from authx import AuthXConfig, AuthX
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette.responses import Response

from src.api.dependencies import SessionDep
from src.models.users import User
from src.schemas.users import UserCreateSchema

router = APIRouter(tags=['Аутентификация'])
auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = 'SECRET_KEY'
auth_config.JWT_ACCESS_COOKIE_NAME = 'access_token'
auth_config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=auth_config)


@router.post('/auth/login', summary='Аутентификация пользователя')
async def login(user: UserCreateSchema, session: SessionDep, response: Response):
    query = select(User).filter(User.name == user.name)
    res = await session.execute(query)
    check_user = res.scalar()
    if check_user.password == user.password:
        token = security.create_access_token(uid=check_user.name)
        response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise HTTPException(401, detail={'message': 'Bad credentials'})


@router.post('/auth/register', summary='Регистрация пользователя')
async def register(user: UserCreateSchema, session: SessionDep, response: Response):
    new_user = User(
        name=user.name,
        password=user.password
    )
    session.add(new_user)
    await session.commit()
    token = security.create_access_token(uid=new_user.name)
    response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)
    return {'ok': True}
