import sys
import fastapi
from fastapi import (FastAPI, Request, Response, status, __version__ as fastapi_version)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from tmp.sub import grand_son_app

app = FastAPI(
    debug=True,
)

app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
async def root():
    return {"Hello": "World!"}

@app.get("/resource/path/{file}")
async def http_url(*, request: Request, key1, key2):
    response = {
        "协议名称": request.url.scheme,
        "主机名": request.url.hostname,
        "端口": request.url.port,
        "资源路径": request.url.path,
        "参数": request.url.query,
        "key1的值": key1,
        "key2的值": key2,
        "请求头部": request.headers,
        "请求体": await request.body(),
    }
    return response

@app.get("/show_me_the_cookie")
async def show_me_the_cookie(response: Response):
    response.set_cookie(key="fake_session_id", value="202409151557", expires=15)
    return {"响应信息":"我们有了cookie了"}

@app.get("/server-status", include_in_schema=False)
async def server_status(*, request: Request, response: Response, token: str | None = None):

    if token == "TOKEN":
        data = {
            "运行状态": "正常运行",
            "fastAPI 版本": fastapi_version,
            "Python 版本": sys.version,
            "request.headers" : request.headers,
        }
        return data
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":"Not Found"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("tmp/fav.png")



son_app = FastAPI()

@son_app.get("/")
async def root():
    return {"data": "我是子应用，独立存在！"}

@son_app.get("/info")
async def info():
    return {"data":"这个是子应用son返回来的信息！"}

app.mount("/son", son_app, name="son")

son_app.mount("/grand_son_app", grand_son_app, name="grand_son_app")


