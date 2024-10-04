import uuid
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime, timezone

from bot.core.db.init_db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        index=True,
    )
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    invited_person = Column(Integer, default=0)
    joined_at = Column(
        DateTime, default=datetime.now(timezone.utc).replace(microsecond=0)
    )
    silence_for = Column(DateTime, default=None)
