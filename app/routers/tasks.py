from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.schemas import TaskCreate, TaskUpdate
from app.crud import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task
)
from app.rate_limiter import rate_limit

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("")
async def create_new_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session)
):
    return await create_task(session, task)

@router.get("")
async def fetch_tasks(
    request: Request,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    status: str = None,
    session: AsyncSession = Depends(get_session)
):
    await rate_limit(request)

    skip = (page - 1) * limit

    return await get_tasks(
        session,
        skip,
        limit,
        status
    )

@router.get("/{task_id}")
async def fetch_task(
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    await rate_limit(request)

    task = await get_task(session, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@router.put("/{task_id}")
async def update_existing_task(
    task_id: int,
    data: TaskUpdate,
    session: AsyncSession = Depends(get_session)
):
    task = await get_task(session, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return await update_task(session, task, data)

@router.delete("/{task_id}")
async def delete_existing_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    task = await get_task(session, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    await delete_task(session, task)

    return {
        "message": "Task deleted successfully"
    }