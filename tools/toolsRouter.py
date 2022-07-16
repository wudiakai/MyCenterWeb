from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from starlette.requests import Request

import tools.toolsDispatcher
from tools import toolsDispatcher

router = APIRouter(prefix="/tools")


@router.get("/")
async def index(req: Request):
    print(req)
    print(req.cookies)
    return {"msg": "tools index!"}


@router.post("/config")
async def make_config(req: Request, file: UploadFile = File(...)):
    # print('type', file.content_type)
    # todo: 增加session控制每次会话，避免重复处理
    res = await tools.toolsDispatcher.dispatcher('config', file)
    if res == 'OK':
        # out_file = await toolsDispatcher.get_out_file('config')
        # return FileResponse(path=out_file, filename='config.zip')
        return {"msg": 'OK'}
    else:
        return {"msg": res}


@router.post("/vhal")
async def make_vhal(req: Request, file: UploadFile = File(...)):
    # print('type', file.content_type)
    # todo: 增加session控制每次会话，避免重复处理
    res = await tools.toolsDispatcher.dispatcher('vhal', file)
    if res == 'OK':
        # out_file = await toolsDispatcher.get_out_file('config')
        # return FileResponse(path=out_file, filename='config.zip')
        return {"msg": 'OK'}
    else:
        return {"msg": res}


@router.get("/config/{session}")
async def get_out_files(req: Request, session: str):
    file = await toolsDispatcher.get_out_file(session)
    print(file)
    return FileResponse(path=file, filename=session + '.zip')
