from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/tools")


@router.get("/")
async def index():
    return {"msg": "tools index!"}


@router.post("/config")
async def make_config(file: UploadFile = File(...)):
    print('type', file.content_type)
    # application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
    print(file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return {"filename": file.filename}
