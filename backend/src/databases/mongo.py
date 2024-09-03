from motor.motor_asyncio import AsyncIOMotorClient
from config import config


class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db_name = None

    async def connect(self):
        self.client = AsyncIOMotorClient(config.MONGODB_URI)
        self.db_name = config.MONGODB_NAME

    async def get_db(self):
        return self.client[self.db_name]

    async def get_server_info(self):
        return await self.client.server_info()

    async def close(self):
        self.client.close()


mongo_connection = MongoDBConnection()
