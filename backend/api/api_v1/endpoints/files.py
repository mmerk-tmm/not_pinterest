import os
from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse

from backend.db.db import get_db
from backend.db.session import SessionLocal
from backend.crud.crud_file import file_cruds
from backend.core.config import settings

router = APIRouter(prefix=settings.UPLOADS_ROUTE, tags=['Файлы'])


@router.get('/images/{image_id}', response_class=FileResponse)
def get_image(image_id):
    db_image = file_cruds.get_image_by_id(image_id=image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.IMAGES_FOLDER,
                             image_id+settings.IMAGES_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/other/{file_id}', response_class=FileResponse)
def get_image(file_id):
    db_file = file_cruds.get_file_by_id(file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.OTHER_FILES_FOLDER,
                             file_id+db_file.extension)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")
