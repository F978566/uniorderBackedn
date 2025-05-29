import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi import HTTPException


files_router = APIRouter(prefix="/files", tags=["files"])


@files_router.get("/{filename}")
async def get_file(filename: str):
    file_path = os.path.join("uploads", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
