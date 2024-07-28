from fastapi import APIRouter, HTTPException
from models import Task, UpdateTaskModel, TaskList
from db import db

tasks_router = APIRouter()


@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    """
    Create a new task.

    This endpoint allows creating a new task by providing the task details.

    Args:
        task (Task): The task object containing the details of the task to be created.

    Returns:
        Task: The created task object.

    Raises:
        HTTPException: If there's an error while creating the task.
    """
    return db.add_task(task)



"""
Get a task by its ID.

This endpoint allows retrieving a task by its unique identifier.

Args:
    task_id (int): The ID of the task to retrieve.

Returns:
    Task: The task object with the specified ID.

Raises:
    HTTPException: If the task with the specified ID is not found.
"""
@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


"""
Get a list of all tasks.

This endpoint allows retrieving a list of all tasks that have been created.

Returns:
    TaskList: A list of all tasks.
"""
@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)


"""
Update a task by its ID.

This endpoint allows updating an existing task by its unique identifier.

Args:
    task_id (int): The ID of the task to update.
    task_update (UpdateTaskModel): The updated task details.

Returns:
    Task: The updated task object.

Raises:
    HTTPException: If the task with the specified ID is not found.
"""
@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

"""
Delete all tasks.

This endpoint allows deleting all tasks that have been created.

Returns:
    dict: A message indicating that all tasks have been deleted successfully.
"""
@tasks_router.delete("/all")
async def delete_all_tasks():
    try:
        db.delete_all_tasks()
        return {"message": "Todas las tareas han sido eliminadas"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar todas las tareas: {str(e)}")


"""
Delete a task by its ID.

This endpoint allows deleting an existing task by its unique identifier.

Args:
    task_id (int): The ID of the task to delete.

Returns:
    dict: A message indicating that the task has been deleted successfully.
"""@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    try:
        task = db.get_task(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        db.delete_task(task_id)
        return {"message": "Tarea eliminada exitosamente"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la tarea: {str(e)}")



