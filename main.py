from fastapi import FastAPI, UploadFile, File
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

import tools.toolsRouter
from markdown import mdRouter, mdManager

app = FastAPI()
app.include_router(mdRouter.router)
app.include_router(tools.toolsRouter.router)
register_tortoise(app,
                  db_url="mysql://likai:!QAZ1qaz@127.0.0.1:3306/fastapi",
                  # db_url="mysql://likai:!QAZ1qaz@localhost:3306/fastapi",
                  modules={"models": ["dao.models"]},
                  add_exception_handlers=True,
                  generate_schemas=True)

origins = [
    "http://10.1.29.*:*",
    "http://10.1.29.11:2020",
    "http://10.1.79.81:2020",
    # "http://localhost",
    # "http://localhost:2020",
    # "http://localhost:2020",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return "Welcome to Android Center!"


@app.on_event('startup')
def init():
    mdManager.init()


if __name__ == '__main__':
    init()
    uvicorn.run(app, host='0.0.0.0', port=2022, debug=True, lifespan='on')
