from sqlmodel import select
from app.models import Task

async def create_task(session, task_data):
    task = Task(**task_data.dict())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_tasks(session, skip, limit, status=None):

    query = select(Task)

    if status:
        query = query.where(Task.status == status)

    tasks = (await session.exec(
        query.offset(skip).limit(limit)
    )).all()

    total = len(tasks)

    return {
        "total": total,
        "tasks": tasks
    }

async def get_task(session, task_id):
    return await session.get(Task, task_id)

async def update_task(session, task, data):

    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)

    await session.commit()
    await session.refresh(task)

    return task

async def delete_task(session, task):
    await session.delete(task)
    await session.commit()