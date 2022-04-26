from fastapi import APIRouter

router = APIRouter(prefix="/tools")


@router.get("/")
async def index():
    return {"msg": "tools index!"}