import sys
from fastapi import (FastAPI, Request, Response, status, __version__ as fastapi_version)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pygments.lexers import templates

from starlette.responses import HTMLResponse

from config import Settings, config

app = FastAPI(
    debug=config.DEBUG_MOOD,
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

@app.get("/post")
async def post(request: Request):
    data = {
        "site" : Site(),
        "page" : page,
        "id" : 1
    }
    return templates.TemplateResponse(name="post.html", context=data, request=request)

@app.get("/videos/{video_id}")
async def videos_function(request: Request,
                          video_id : int,
                          ):
    if video_id > 1 or video_id < 1:
        video_id = None

    data = {

    }
    return templates.TemplateResponse(name="videos.html", context=data, request=request)

@app.get("/post_v1")
async def post_html_v1():
    data = f'''

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link href="http://120.0.0.1:8080/static/css/main.css" rel="stylesheet">
</head>
<body>
    <h1>这个是Post画面</h1>
    <article>
        <header>这是一篇文章</header>
        <section>这篇文章的具体内容，标题和文章主体部分都是可变的。</section>
    </article>
</body>
</html>

'''
    return HTMLResponse(content=data)

@app.get("/post_v2")
async def post_html_v2():
    name = "FastAPI开发与部属"
    id = 1
    title = '这是一篇文章v2'
    body = '这篇文章的具体内容，标题和文章主体部分都是可变的。'
    data = f'''

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{name}</title>
    <link href="http://120.0.0.1:8080/static/css/main.css" rel="stylesheet">
</head>
<body>
    <h1>这个是Post画面</h1>
    <article>
        <header>{title}</header>
        <section>{body}</section>
    </article>
</body>
</html>

'''
    return HTMLResponse(content=data)


def html_maker(*, content:dict, request:Request):
    globals().update(content)
    data = f'''

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{name}</title>
        <link href="{request.url_for('static', path='/css/main.css')}" rel="stylesheet">
    </head>
    <body>
        <h1>这个是Post画面</h1>
        <article>
            <header>{title}</header>
            <section>{body}</section>
        </article>
    </body>
    </html>

    '''
    return HTMLResponse(content=data, status_code=status.HTTP_200_OK)


@app.get("/post_v3", response_class=HTMLResponse)
async def post_html_v3(request: Request):
    data = {
        "name" : "FastAPI开发与部属",
        "id" : 1,
        "title" : '这是一篇文章v3',
        "body" : '这篇文章的具体内容，标题和文章主体部分都是可变的。',
    }
    return html_maker(content=data, request=request)