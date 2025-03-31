from dns.e164 import query
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from src.api.auth import security
from src.api.dependencies import SessionDep
from src.database import engine, Base
from src.models.users import User
from src.schemas.jobs import JobGetSchema
from src.schemas.users import UserGetSchema

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

@router.get('/users/{id}', summary='Получить одного пользователя')
async def get_one_user(id: int, session: SessionDep):
    query = select(User).filter(User.id == id)
    data = await session.execute(query)
    res_user = data.scalar()
    if not res_user:
        raise HTTPException(404, 'User not found')
    return res_user

@router.put('/users/add_job/{id}', summary='Добавить работу')
async def add_job_to_user(id: int, job: JobGetSchema, session: SessionDep):
    query = select(User).filter(User.id == id)
    data = await session.execute(query)
    res_user = data.scalar()
    if not res_user:
        raise HTTPException(404, 'User not found')
    res_user.job = job.id
    return {'ok': True}