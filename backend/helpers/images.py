from uuid import UUID
from backend.models.files import Image
from backend.core.config import settings
import io
from PIL import Image as pillow
import logging
import shutil
from fastapi import UploadFile, HTTPException
from backend.crud.crud_file import FileCRUD
from sqlalchemy.orm import Session
from pathlib import Path
logger = logging.getLogger(__name__)
supported_image_extensions = {
    ex for ex, f in pillow.registered_extensions().items() if f in pillow.OPEN}


def set_picture(data: dict, picture: Image):
    if picture:
        data['picture'] = ''.join(
            [settings.SERVER_LINK, settings.API_V1_STR,  settings.UPLOADS_ROUTE, '/images/', str(picture.id)])
    return data


def save_image(db: Session, upload_file: UploadFile, user_id: int, resize_image_options=(400, 400), bytes_io_file: io.BytesIO = None, detail_error_message="поврежденное изображение"):
    if not bytes_io_file and (not upload_file or not upload_file.filename):
        return
    if bytes_io_file:
        originalFileName = bytes_io_file.name
    else:
        originalFileName = upload_file.filename
    originalFilePath = Path(originalFileName)
    suffix = originalFilePath.suffix
    if suffix.lower() not in supported_image_extensions:
        raise HTTPException(
            status_code=422, detail="Расширение изображения не поддерживается")
    if bytes_io_file:
        buf = bytes_io_file
    else:
        buf = io.BytesIO()
        shutil.copyfileobj(upload_file.file, buf)
        buf.seek(0)

    try:
        image = pillow.open(buf)
        image.thumbnail(resize_image_options)
        image_model = FileCRUD(db).create_image(
            width=image.width, height=image.height, user_id=user_id)
        image.save(image_id_to_path(image_model.id))
        return image_model
    except:
        raise HTTPException(status_code=422, detail=detail_error_message)


def image_id_to_path(image_id: int) -> str:
    return '/'.join([settings.IMAGES_FOLDER, str(image_id)+settings.IMAGES_EXTENTION])


def image_id_to_url(image_id: UUID) -> str:
    return ''.join([settings.API_V1_STR, settings.UPLOADS_ROUTE, '/images/', str(image_id)])
