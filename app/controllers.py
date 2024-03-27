from typing import List
from fastapi import HTTPException
from app.database import get_collection
from app.model import Task
from bson import json_util
from bson.objectid import ObjectId
import json
from config import settings

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
    print('settings.MONGO_URI')
    print(settings.MONGO_URI)
    print('settings.MONGO_URI')
    try:
        filters = {}
        all_filters = []
        if title:
            all_filters.append({"title": title})
        if description:
            all_filters.append({"description": description})
        if author:
            all_filters.append({"auther": author})

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

        return serialized_results

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
