from fastapi import FastAPI

grand_son_app = FastAPI()

@grand_son_app.get("/")
async def info():
    return {"data": "我是子应用son_app的子应用！"}

@grand_son_app.get("/info")
async def info():
    return {"data" : "我是grand_son_app这个应用的info路径！"}