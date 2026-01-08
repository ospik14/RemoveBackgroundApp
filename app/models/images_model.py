from sqlalchemy import ForeignKey, String
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Images(Base):

    __tablename__ = 'images'
    id: Mapped[int] = mapped_column(primary_key=True)
    original_name: Mapped[str] =  mapped_column(String(50))
    original_filename: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    processed_filename: Mapped[str] =  mapped_column(String(100), unique=True, index=True)
    owner_id: Mapped[int] =  mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] 