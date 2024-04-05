from fastapi import FastAPI
from routers import products,users

app = FastAPI()
# Url Local: http://127.0.0.1:8000/

# Routers
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
async def read_root():
    return "Hola Mundo FastAPI "


@app.get("/url")
async def read_url():
    return {"url": "https://mouredev.com/python"}
