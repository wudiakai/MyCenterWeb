from fastapi import APIRouter

router = APIRouter(prefix="/user")


@router.get("/")
async def index():
    return {"msg": "user index!"}