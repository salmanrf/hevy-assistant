from src.databases.mongo import mongo_connection
from .models.user import UserModel


async def find_one_user(criteria: dict) -> UserModel:
    try:
        db = await mongo_connection.get_db()

        result = await db["users"].find_one(criteria)

        if not result:
            return None

        user = UserModel(**result)

        return user
    except Exception as e:
        print("Error at find_one_user", e)

        raise e


async def create_user(user_dto: UserModel) -> UserModel:
    try:
        db = await mongo_connection.get_db()

        user_data = user_dto.model_dump(exclude=["id"])

        result = await db["users"].insert_one(user_data)
        created = await find_one_user({"_id": result.inserted_id})

        return created
    except Exception as e:
        print("Error at create_user", e)

        raise e


async def find_or_create_user(user_dto: UserModel) -> UserModel:
    try:
        existing = await find_one_user({"hevy_user_id": user_dto.hevy_user_id})

        if existing:
            return existing

        new_user = await create_user(user_dto)

        return new_user
    except Exception as e:
        print("Error at find_one_or_create_user", e)

        raise e
