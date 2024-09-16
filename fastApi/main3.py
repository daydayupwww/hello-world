import hashlib
import sys
import time
from doctest import master
from functools import lru_cache

from fastapi import (FastAPI, Request, Response, status, __version__ as fastapi_version, UploadFile, Query)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pygments.lexers import templates

from starlette.responses import HTMLResponse

from config import Settings, config

app = FastAPI(
    debug=True,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

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

class Site(BaseModel):
    name: str = "FastAPI开发部署"


page = {
    "title" : "这是一篇文章",
    "body":"这篇文章的具体内容部分，标题和文章主体部分都是可变的。"
}


@lru_cache(maxsize=5)
def lru_test(change):
    print("lru_test")
    time.sleep(8)
    data = {
        "site" : Site(),
        "page" : page,
        "id" : 1
    }
    print("sleep 8")
    return data

@app.get("/post/{change}")
async def post(request: Request, change: int):
    # data = {
    #     "site" : Site(),
    #     "page" : page,
    #     "id" : 1
    # }
    data = lru_test(change)
    print(lru_test.cache_info())
    return templates.TemplateResponse(name="post.html", context=data, request=request)

@app.post("/upload_file/{path_var}", summary="upload file")
async def upload_file(*,
                      file: UploadFile,
                      path_var: str | None = None,
                      code: str | None = Query(None, min_length=3, max_length=3, alias="token")
                      ):
    file_local = await save_files(file)
    return {"file name": file.filename,
            "content_type": file.content_type,
            "path_var": path_var,
            "code": code,
            "file_load": file_local}

async def save_files(file):
    path = "files/"
    res = await file.read()
    hash_name = hashlib.md5(file.filename.encode()).hexdigest()[:8]
    file_name = f"{hash_name}.{file.filename.rsplit('.', 1)[1]}"
    full_file = f"{path}{file_name}"
    with open(full_file, "wb") as f:
        f.write(res)
    return full_file