from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/users",
                   tags= ["users"],
                   responses={404: {"message": "No encontrado"}})


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    url: str


users = [
    User(id=1, name="Robin", surname="Espinoza",
         age=29, url="https://robin.com"),
    User(id=2, name="Joaquin", surname="Espinoza",
         age=1, url="https://quin.com"),
    User(id=3, name="Katy", surname="Lazaro",
         age=31, url="https://katy.com")
]


@router.get("/json")
async def get_usersjson():
    return [{"name": "Robin", "surname": "Espinoza", "url": "https://robin.com"},
            {"name": "Joaquin", "surname": "Espinoza", "url": "https://quin.com"},
            {"name": "Katy", "surname": "Lazaro", "url": "https://katy.com"}]


@router.get("/")
async def get_users():
    return users


@router.get("/{id}")  # Path
async def get_user(id: int):
    return search_user(id)


@router.get("/query/")  # Query
async def get_user(id: int):
    return search_user(id)


@router.post("/", status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(
            status_code=409,
            detail="El usuario ya existe"
            )
        # return {"status": False, "message": "El usuario ya existe"}
    else:
        users.append(user)
        return user


@router.put("/")
async def update_user(user: User):
    matching_users = list(filter(
        lambda saved_user: saved_user.id == user.id, users)
    )
    if len(matching_users) > 0:
        is_updated = update_user(user)
        if is_updated:
            return user
        else:
            return {"status": False, "message": "No se ha podido actualizar el usuario"}
    else:
        return {"status": False, "message": "El usuario que desea actualizar no existe"}


@router.delete("/{id_user}")
async def delete_user(id_user: int):
    matching_users = list(filter(
        lambda saved_user: saved_user.id == id_user, users)
    )
    if len(matching_users) > 0:
        is_deleted = delete_user(id_user)
        if is_deleted:
            return {"status": True, "message": "Se ha eliminado el usuario"}
        else:
            return {"status": False, "message": "No se ha podido eliminar el usuario"}
    else:
        return {"status": False, "message": "El usuario que desea eliminar no existe"}


def search_user(id: int):
    filtered_users = filter(lambda user: user.id == id, users)
    try:
        user_selected = list(filtered_users)[0]
        return user_selected
        # return f"El nombre del usuario es {user_selected.name} y tiene {user_selected.age} años"
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
