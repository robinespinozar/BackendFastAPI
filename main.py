from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# Url Local: http://127.0.0.1:8000/

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return "Hola Mundo FastAPI "


@app.get("/url")
async def read_url():
    return {"url": "https://mouredev.com/python"}
