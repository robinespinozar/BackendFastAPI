from fastapi import FastAPI

app = FastAPI()
# Url Local: http://127.0.0.1:8000/

@app.get("/")
async def read_root():
    return "Hola Mundo FastAPI "

@app.get("/url")
async def read_url():
    return {"url":"https://mouredev.com/python"}