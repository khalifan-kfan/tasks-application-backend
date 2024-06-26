from typing import List
from fastapi import HTTPException
from app.database import get_collection
from app.model import Task, TaskUpdate
from bson import json_util
from bson.objectid import ObjectId
import json
from config import settings
from fastapi.responses import JSONResponse
from datetime import datetime


def add_task(data: dict = {}):
    try:
        task = Task(**data)
        task.creation_date = datetime.now().isoformat()
        added_data = get_collection().insert_one(task.dict())
        return {"task_id": str(added_data.inserted_id)}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})


def get_tasks(title: str, description: str, author: str,
              before: str, after: str, page: int = 1, limit: int = 10) -> List[dict]:
    try:
        filters = {}
        all_filters = []
        if title:
            all_filters.append({"title": {"$regex": title, "$options": "i"}})
        if description:
            all_filters.append(
                {"description": {"$regex": description, "$options": "i"}})
        if author:
            all_filters.append({"author": {"$regex": author, "$options": "i"}})

        if after:
            all_filters.append({
                "deadline": {
                    "$gte": datetime.strptime(after, "%Y-%m-%d")
                }
            })
        if before:
            all_filters.append({
                "deadline": {
                    "$lte": datetime.strptime(before, "%Y-%m-%d")
                }
            })

        if all_filters:
            filters["$and"] = all_filters

        # Calculate the skip value based on the page and limit
        skip = (page - 1) * limit

        # Perform pagination by using skip and limit in the query
        results = get_collection().find(filters).skip(skip).limit(limit)

        serialized_results = json.loads(json_util.dumps(results))

        total_count = get_collection().count_documents(filters)

        total_pages = (total_count + limit - 1) // limit

        pagination = {
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "limit": limit
        }

        return {
            "data": serialized_results,
            "pagination": pagination
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})


def get_single_task(task_id: str):
    try:
        task = get_collection().find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail={
                                "message": "Task not found or does not exist"})
        return task
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})


def update_task(task_id: str, task_update: dict = {}):
    print(task_update.dict())
    try:
        updated_task_dict = task_update.dict(exclude_unset=True)

        updated_task_dict = {k: v for k,
                             v in updated_task_dict.items() if v is not None}

        updated_task = get_collection().find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": updated_task_dict},
            return_document=True
        )
        if updated_task:
            updated_task['_id'] = str(updated_task['_id'])
            updated_task['deadline'] = updated_task['deadline'].isoformat(
            ) if updated_task.get('deadline') else None
            return JSONResponse(content=updated_task)
        return None
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
                            "message": "Internal server error"})
