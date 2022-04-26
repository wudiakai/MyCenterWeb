import asyncio
import threading

from fastapi import FastAPI, UploadFile, File
import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from dao.models import MyMarkdown
from markdown import mdRouter

app = FastAPI()
app.include_router(mdRouter.router)
register_tortoise(app,
                  # db_url="mysql://likai:!QAZ1qaz@localhost:3306/fastapi",
                  db_url="mysql://root:123456@localhost:3306/fastapi",
                  modules={"models": ["dao.models"]},
                  add_exception_handlers=True,
                  generate_schemas=True)


@app.get("/")
async def index():
    res = await MyMarkdown().all()
    print(res)
    print(len(res))
    print(res[0].content)
    print(type(res))
    return "Welcome to Android Center!"

def init():
    # mdManager.init()
    pass


if __name__ == '__main__':
    init()
    uvicorn.run(app, host='0.0.0.0', port=2022, debug=True, lifespan='on')
