from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/usersdb",
                   tags=["usersdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


users = []


@router.get("/", response_model=list[User],description="HOLAS MSNERAKSD")
async def get_users():
    return users_schema(db_client.local.users.find())


@router.get("/{id}")  # Path
async def get_user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/query/")  # Query
async def get_user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya existe"
        )

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", response_model=User)
async def update_user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.local.users.find_one_and_replace(
            filter={"_id": ObjectId(user.id)},
            replacement=user_dict
        )
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))


@router.delete("/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id_user: str):

    found = db_client.local.users.find_one_and_delete(
        {"_id": ObjectId(id_user)}
    )

    if not found:
        return {"error": "No se ha eliminado el usuario"}


def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"status": False, "message": "No se ha encontrado al usuario"}


def update_user(updated_user: User) -> bool:
    found = False
    try:
        for index, saved_user in enumerate(users):
            if saved_user.id == updated_user.id:
                users[index] = updated_user
                found = True
    except:
        return False

    return found


def delete_user(id_user: int) -> bool:
    found = False
    try:
        for index, saved_user in enumerate(users):
            if saved_user.id == id_user:
                del users[index]
                found = True
    except:
        return False

    return found
