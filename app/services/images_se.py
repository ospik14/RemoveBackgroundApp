import os
import aiofiles
from rembg import remove
from fastapi.concurrency import run_in_threadpool
from fastapi import UploadFile
from models.images_model import Images
from core.security import get_unique_name
from repositories.images_db import add_image_to_db, get_all_images
from datetime import datetime, timezone

UPLOAD_DIR = 'media/'

async def remove_background(input_image: bytes):
    output_image = await run_in_threadpool(remove, input_image)

    return output_image

async def save_image(image: bytes, extension: str):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
 
    unique_name = f'{get_unique_name()}.{extension}'
    current_path = f'{UPLOAD_DIR}{unique_name}'

    async with aiofiles.open(current_path, 'wb') as out_file:
        await out_file.write(image)

    return unique_name

async def processing_image(db, user, image: UploadFile):
    extension = image.filename.split('.')[-1]
    image_bytes = await image.read()

    processed_image = await remove_background(image_bytes)
    original_fn = await save_image(image_bytes, extension)
    processed_fn = await save_image(processed_image, 'png')

    current_image = Images(
        original_name = image.filename,
        original_filename = original_fn,
        processed_filename = processed_fn,
        owner_id = user.user_id,
        created_at = datetime.now(timezone.utc).replace(tzinfo=None)
    )

    await add_image_to_db(db, current_image)

    return {
        'original_url': f'{UPLOAD_DIR}{original_fn}',
        'processed_url': f'{UPLOAD_DIR}{processed_fn}'
    }

async def get_images(db, user):
    images = await get_all_images(db, user.user_id)
    if not images: return []
    return [
        {
            'id': image.id,
            'name': image.original_name,
            'original_url': f'{UPLOAD_DIR}{image.original_filename}',
            'processed_url': f'{UPLOAD_DIR}{image.processed_filename}',
            'created_at': image.created_at
        }
        for image in images
    ]
    