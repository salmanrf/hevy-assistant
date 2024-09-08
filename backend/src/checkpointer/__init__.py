from config import config
from src.databases.mongo import mongo_connection
from .mongo_saver import AsyncMongoDBSaver

mongodb_checkpointer = AsyncMongoDBSaver(mongo_connection.client, config.MONGODB_NAME)
