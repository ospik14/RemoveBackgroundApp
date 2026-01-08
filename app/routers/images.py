from fastapi import APIRouter, File, UploadFile
from typing import Annotated
from services.images_se import processing_image, get_images
from dependencies import user_dep, db_dep

router = APIRouter(
    prefix='/images',
    tags=['images']
)

@router.post('/remove')
async def remove_bg(db: db_dep, user: user_dep, image: Annotated[UploadFile, File()]):
    if not image.content_type.startswith('image/'):
        return {'error': 'file type not image'}
    result = await processing_image(db, user, image)

    return  result

@router.get('/get_all')
async def get_all_images(db: db_dep, user: user_dep):
    return await get_images(db, user)