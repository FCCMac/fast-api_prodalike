from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path

from app.static_values import MONGO_ID_REGEX
from app.utilities.db import db

from .models import NotFoundException, Todo, TodoId, TodoRecord


router = APIRouter()


@router.post("", response_model=TodoId)
async def create_todo(payload: Todo) -> TodoId:
    """
    Create a new Todo
    """

    now = datetime.now(timezone.utc)
    insert_result = await db.todos.insert_one(
        {
            "title": payload.title,
            "completed": payload.completed,
            "created_date": now,
            "updated_date": now,
        }
    )

    return TodoId(id=str(insert_result.inserted_id))


@router.get(
    "/{id}",
    response_model=TodoRecord,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def get_todo(
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX)
) -> TodoRecord:
    """
    Get a Todo
    """

    doc = await db.todos.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not Found")

    return TodoRecord(
        id=str(doc["_id"]),
        title=doc["title"],
        completed=doc["completed"],
        created_date=doc["created_date"],
        updated_date=doc["updated_date"],
    )


@router.get("", response_model=list[TodoRecord])
async def get_todos() -> list[TodoRecord]:
    """
    Get Todos
    """

    todos: list[TodoRecord] = []
    async for doc in db.todos.find():
        todos.append(
            TodoRecord(
                id=str(doc["_id"]),
                title=doc["title"],
                completed=doc["completed"],
                created_date=doc["created_date"],
                updated_date=doc["updated_date"],
            )
        )

    return todos


@router.put(
    "/{id}",
    response_model=TodoId,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def update_todo(
    payload: Todo,
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> TodoId:
    """
    Update a Todo
    """

    now = datetime.now(timezone.utc)
    update_result = await db.todos.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": payload.title,
                "completed": payload.completed,
                "updated_date": now,
            }
        },
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return TodoId(id=id)


@router.delete(
    "/{id}",
    response_model=bool,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def delete_todo(
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> bool:
    """
    Delete a todo
    """

    delete_result = await db.todos.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return True
