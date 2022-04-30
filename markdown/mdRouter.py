from fastapi import APIRouter
from pydantic import BaseModel
from dao.models import MyMarkdown
from markdown import mdManager

router = APIRouter()


class Response(BaseModel):
    msg: str = 'ok'
    code: int = 200
    data: str = ''


@router.get("/sync")
async def sync_svn():
    """sync from svn """
    await mdManager.refresh()
    return {"msg", "OK"}


@router.get("/markdownList/{item}")
async def get_md_list(item: str):
    return mdManager.read_markdown_list(item)


@router.get("/search/{text}")
async def search_text(text: str):
    res = await mdManager.search(text)
    return res


@router.get("/content/{name}", response_model=Response)
async def get_content(name: str):
    res = await mdManager.get_data_by_name(name)
    if isinstance(res, MyMarkdown):
        return {'data': res.content}
    else:
        return {'data': "This article was not found!"}
