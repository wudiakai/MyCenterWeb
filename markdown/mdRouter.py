from fastapi import APIRouter

from dao.models import MyMarkdown
from markdown import mdManager

router = APIRouter()


@router.get("/sync")
async def syncSvn():
    await mdManager.refresh()
    return {"msg", "OK"}


@router.get("/content/{name}")
async def getContent(name: str):
    res = await mdManager.getDataByName(name)
    if isinstance(res, MyMarkdown):
        return res.content
    else:
        return "This article was not found!"
