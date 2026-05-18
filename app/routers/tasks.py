from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional

from app.database import get_session
from app.logger import logger
from app.schemas import DeleteResponse, TaskCreate, TaskListResponse, TaskRead, TaskStatus, TaskUpdate
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

@router.post("", response_model=TaskRead, status_code=201)
async def create_new_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session)
):
    created_task = await create_task(session, task)
    logger.info("Created task id=%s", created_task.id)
    return created_task

@router.get("", response_model=TaskListResponse)
async def fetch_tasks(
    request: Request,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    status: Optional[TaskStatus] = None,
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

@router.get("/{task_id}", response_model=TaskRead)
async def fetch_task(
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    await rate_limit(request)

    task = await get_task(session, task_id)

    if not task:
        logger.warning("Task not found id=%s", task_id)
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@router.put("/{task_id}", response_model=TaskRead)
async def update_existing_task(
    task_id: int,
    data: TaskUpdate,
    session: AsyncSession = Depends(get_session)
):
    task = await get_task(session, task_id)

    if not task:
        logger.warning("Task not found for update id=%s", task_id)
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    updated_task = await update_task(session, task, data)
    logger.info("Updated task id=%s", updated_task.id)
    return updated_task

@router.delete("/{task_id}", response_model=DeleteResponse)
async def delete_existing_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    task = await get_task(session, task_id)

    if not task:
        logger.warning("Task not found for delete id=%s", task_id)
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    await delete_task(session, task)
    logger.info("Deleted task id=%s", task_id)

    return {
        "message": "Task deleted successfully"
    }
