from pymongo.mongo_client import MongoClient
from config import settings

mongo = MongoClient(settings.MONGO_URI, port=None, connect=True)

database_name = 'tasks_db'
if settings.FASTAPI_ENV == 'testing':
    database_name = 'testing_tasks_db'

try:
    mongo_db = mongo.get_database(database_name)
except Exception as e:
    mongo_db = mongo.get_database('testing_tasks_db')


def get_collection():
    return mongo_db["tasks"]
