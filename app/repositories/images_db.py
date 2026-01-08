from models.images_model import Images
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def add_image_to_db(db: AsyncSession, image: Images):
    db.add(image)
    await db.commit()
    await db.refresh(image)

async def get_all_images(db: AsyncSession, user_id: int):
    query = select(Images).filter(Images.owner_id == user_id)
    images = await db.execute(query)

    return images.scalars().all()