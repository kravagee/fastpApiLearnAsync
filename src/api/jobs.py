from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from src.api.auth import security
from src.api.dependencies import SessionDep
from src.models.jobs import Job
from src.schemas.jobs import JobGetSchema, JobCreateSchema

router = APIRouter(tags=['Работы'], dependencies=[Depends(security.access_token_required)])


@router.get('/jobs', summary='Получить все работы')
async def get_jobs(session: SessionDep):
    query = select(Job)
    data = await session.execute(query)
    jobs = data.scalars().all()
    return jobs


@router.get('/jobs/{id}', summary='Получить одну работу')
async def get_one_job(id: int, session: SessionDep):
    query = select(Job).filter(Job.id == id)
    data = await session.execute(query)
    res_job = data.scalar()
    if not res_job:
        raise HTTPException(404, 'Job not found')
    return res_job


@router.post('/jobs', summary='Добавить новую работу')
async def create_job(job: JobCreateSchema, session: SessionDep):
    new_job = Job(
        name=job.name,
        description=job.description
    )
    session.add(new_job)
    await session.commit()
    return {'ok': True}