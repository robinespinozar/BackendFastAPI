from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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


@app.get("/usersjson")
async def get_usersjson():
    return [{"name": "Robin", "surname": "Espinoza", "url": "https://robin.com"},
            {"name": "Joaquin", "surname": "Espinoza", "url": "https://quin.com"},
            {"name": "Katy", "surname": "Lazaro", "url": "https://katy.com"}]


@app.get("/users")
async def get_users():
    return users


@app.get("/user/{id}")  # Path
async def get_user(id: int):
    return search_user(id)


@app.get("/userquery/")  # Query
async def get_user(id: int):
    return search_user(id)


def search_user(id: int,name:str):
    filtered_users = filter(lambda user: user.id == id, users)
    try:
        user_selected = list(filtered_users)[0]
        return f"El nombre del usuario es {user_selected.name} y tiene {user_selected.age} años"
    except:
        return {"status": False, "message": "No se ha encontrado al usuario"}
