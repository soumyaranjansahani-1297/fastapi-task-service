from sqlalchemy import func
from sqlmodel import select
from app.models import Task

async def create_task(session, task_data):
    task = Task(**task_data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_tasks(session, skip, limit, status=None):

    query = select(Task)
    count_query = select(func.count()).select_from(Task)

    if status:
        status_value = status.value if hasattr(status, "value") else status
        query = query.where(Task.status == status_value)
        count_query = count_query.where(Task.status == status_value)

    tasks = (await session.exec(
        query.offset(skip).limit(limit)
    )).all()

    total = (await session.exec(count_query)).one()

    return {
        "total": total,
        "tasks": tasks
    }

async def get_task(session, task_id):
    return await session.get(Task, task_id)

async def update_task(session, task, data):

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)

    await session.commit()
    await session.refresh(task)

    return task

async def delete_task(session, task):
    await session.delete(task)
    await session.commit()
