from fastapi import APIRouter, Response, HTTPException, Depends
from sqlalchemy import select

from src.api.auth import security
from src.api.dependencies import SessionDep
from src.database import engine, Base
from src.models.users import User
from src.schemas.users import UserCreateSchema

router = APIRouter(tags=['Пользователи'], dependencies=[Depends(security.access_token_required)])


@router.post('/setup')
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    return {'ok': True}


@router.get('/users', summary='Получить всех пользователей')
async def get_users(session: SessionDep):
    query = select(User)
    data = await session.execute(query)
    users = data.scalars().all()
    return users
